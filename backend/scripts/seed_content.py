#!/usr/bin/env python3
"""
Content Seeding Script

Responsibility: Syncs content JSON files from /content to Supabase database.
Supports dry-run mode to preview changes without applying them.

Usage:
    python -m scripts.seed_content --dry-run     # Preview changes
    python -m scripts.seed_content               # Apply changes
    python -m scripts.seed_content --track systems-foundations  # Seed specific track

Identifier Strategy:
- Tracks: identified by slug (unique)
- Units: identified by (track_id, order_index) - composite unique
- Drills: identified by (unit_id, slug) - composite unique

This ensures content can be renamed, reordered, and updated safely.
"""

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pydantic import ValidationError
from supabase import create_client, Client

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings
from app.schemas.content import TrackContent, UnitContent, DrillContent


# =============================================================================
# DATA STRUCTURES
# =============================================================================


@dataclass
class ContentChange:
    """Represents a pending change to the database."""

    action: str  # "insert" or "update"
    table: str
    identifier: str
    data: dict[str, Any]
    diff: dict[str, tuple[Any, Any]] = field(default_factory=dict)  # field: (old, new)


@dataclass
class ValidationError_:
    """Represents a content validation error."""

    file_path: str
    field: str
    message: str


@dataclass
class SeedResult:
    """Result of the seeding operation."""

    changes: list[ContentChange]
    errors: list[ValidationError_]
    tracks_processed: int = 0
    units_processed: int = 0
    drills_processed: int = 0


# =============================================================================
# CONTENT LOADING
# =============================================================================


def load_json_file(file_path: Path) -> dict[str, Any]:
    """Load and parse a JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_content_dir() -> Path:
    """Find the content directory relative to this script."""
    # Script is in backend/scripts, content is in repo root
    script_dir = Path(__file__).parent
    content_dir = script_dir.parent.parent / "content"

    if not content_dir.exists():
        raise FileNotFoundError(f"Content directory not found: {content_dir}")

    return content_dir


def discover_tracks(content_dir: Path) -> list[Path]:
    """Find all track directories (those containing track.json)."""
    tracks = []
    for track_dir in content_dir.iterdir():
        if track_dir.is_dir() and (track_dir / "track.json").exists():
            tracks.append(track_dir)
    return sorted(tracks)


def load_track_content(track_dir: Path) -> tuple[TrackContent | None, list[ValidationError_]]:
    """Load and validate track.json."""
    errors = []
    track_file = track_dir / "track.json"

    try:
        data = load_json_file(track_file)
        track = TrackContent(**data)
        return track, errors
    except json.JSONDecodeError as e:
        errors.append(ValidationError_(str(track_file), "json", f"Invalid JSON: {e}"))
    except ValidationError as e:
        for err in e.errors():
            field_path = ".".join(str(x) for x in err["loc"])
            errors.append(ValidationError_(str(track_file), field_path, err["msg"]))

    return None, errors


def load_unit_content(unit_file: Path) -> tuple[UnitContent | None, list[ValidationError_]]:
    """Load and validate a unit JSON file."""
    errors = []

    try:
        data = load_json_file(unit_file)
        unit = UnitContent(**data)
        return unit, errors
    except json.JSONDecodeError as e:
        errors.append(ValidationError_(str(unit_file), "json", f"Invalid JSON: {e}"))
    except ValidationError as e:
        for err in e.errors():
            field_path = ".".join(str(x) for x in err["loc"])
            errors.append(ValidationError_(str(unit_file), field_path, err["msg"]))

    return None, errors


def load_drill_content(drill_file: Path) -> tuple[DrillContent | None, list[ValidationError_]]:
    """Load and validate a drill JSON file."""
    errors = []

    try:
        data = load_json_file(drill_file)
        drill = DrillContent(**data)
        return drill, errors
    except json.JSONDecodeError as e:
        errors.append(ValidationError_(str(drill_file), "json", f"Invalid JSON: {e}"))
    except ValidationError as e:
        for err in e.errors():
            field_path = ".".join(str(x) for x in err["loc"])
            errors.append(ValidationError_(str(drill_file), field_path, err["msg"]))

    return None, errors


def discover_units(track_dir: Path) -> list[Path]:
    """Find all unit JSON files in a track directory."""
    units_dir = track_dir / "units"
    if not units_dir.exists():
        return []

    return sorted(units_dir.glob("unit-*.json"))


def discover_drills(track_dir: Path, unit_order_index: int) -> list[Path]:
    """Find all drill JSON files for a given unit."""
    drills_dir = track_dir / "drills" / f"unit-{unit_order_index:02d}"
    if not drills_dir.exists():
        return []

    return sorted(drills_dir.glob("*.json"))


# =============================================================================
# DATABASE OPERATIONS
# =============================================================================


def get_supabase_client() -> Client:
    """Create Supabase client using service role key."""
    return create_client(settings.supabase_url, settings.supabase_service_key)


def fetch_existing_track(client: Client, slug: str) -> dict[str, Any] | None:
    """Fetch a track by slug."""
    response = client.table("tracks").select("*").eq("slug", slug).execute()
    return response.data[0] if response.data else None


def fetch_existing_unit(client: Client, track_id: str, order_index: int, dry_run: bool = False) -> dict[str, Any] | None:
    """Fetch a unit by track_id and order_index."""
    if dry_run and track_id == "DRY_RUN_ID":
        return None
    response = (
        client.table("units")
        .select("*")
        .eq("track_id", track_id)
        .eq("order_index", order_index)
        .execute()
    )
    return response.data[0] if response.data else None


def fetch_existing_drill(client: Client, unit_id: str, slug: str, dry_run: bool = False) -> dict[str, Any] | None:
    """Fetch a drill by unit_id and slug."""
    if dry_run and unit_id == "DRY_RUN_ID":
        return None
    response = (
        client.table("drills")
        .select("*")
        .eq("unit_id", unit_id)
        .eq("slug", slug)
        .execute()
    )
    return response.data[0] if response.data else None


def upsert_track(client: Client, track: TrackContent, dry_run: bool) -> tuple[str, ContentChange | None]:
    """Upsert a track, returning the track ID and any change made."""
    existing = fetch_existing_track(client, track.slug)

    track_data = {
        "slug": track.slug,
        "title": track.title,
        "description": track.description,
    }

    if existing:
        # Check for changes
        diff = {}
        for key, new_val in track_data.items():
            old_val = existing.get(key)
            if old_val != new_val:
                diff[key] = (old_val, new_val)

        if diff:
            change = ContentChange(
                action="update",
                table="tracks",
                identifier=track.slug,
                data=track_data,
                diff=diff,
            )

            if not dry_run:
                client.table("tracks").update(track_data).eq("id", existing["id"]).execute()

            return existing["id"], change
        else:
            return existing["id"], None
    else:
        change = ContentChange(
            action="insert",
            table="tracks",
            identifier=track.slug,
            data=track_data,
        )

        if not dry_run:
            response = client.table("tracks").insert(track_data).execute()
            return response.data[0]["id"], change
        else:
            return "DRY_RUN_ID", change


def upsert_unit(
    client: Client, unit: UnitContent, track_id: str, dry_run: bool
) -> tuple[str, ContentChange | None]:
    """Upsert a unit, returning the unit ID and any change made."""
    existing = fetch_existing_unit(client, track_id, unit.order_index, dry_run)

    unit_data = {
        "track_id": track_id,
        "order_index": unit.order_index,
        "title": unit.title,
        "summary_markdown": unit.summary_markdown,
    }

    if existing:
        diff = {}
        for key, new_val in unit_data.items():
            old_val = existing.get(key)
            if old_val != new_val:
                diff[key] = (old_val, new_val)

        if diff:
            change = ContentChange(
                action="update",
                table="units",
                identifier=f"{unit.track_slug}/unit-{unit.order_index}",
                data=unit_data,
                diff=diff,
            )

            if not dry_run:
                client.table("units").update(unit_data).eq("id", existing["id"]).execute()

            return existing["id"], change
        else:
            return existing["id"], None
    else:
        change = ContentChange(
            action="insert",
            table="units",
            identifier=f"{unit.track_slug}/unit-{unit.order_index}",
            data=unit_data,
        )

        if not dry_run:
            response = client.table("units").insert(unit_data).execute()
            return response.data[0]["id"], change
        else:
            return "DRY_RUN_ID", change


def upsert_drill(
    client: Client, drill: DrillContent, unit_id: str, unit_identifier: str, dry_run: bool
) -> tuple[str, ContentChange | None]:
    """Upsert a drill, returning the drill ID and any change made."""
    existing = fetch_existing_drill(client, unit_id, drill.slug, dry_run)

    drill_data = {
        "unit_id": unit_id,
        "slug": drill.slug,
        "drill_type": drill.drill_type.value,
        "prompt_markdown": drill.prompt_markdown,
        "rubric": drill.rubric.model_dump(),
        "difficulty": drill.difficulty,
        "estimated_minutes": drill.estimated_minutes,
        "concept_tags": drill.concept_tags,
    }

    identifier = f"{unit_identifier}/{drill.slug}"

    if existing:
        diff = {}
        for key, new_val in drill_data.items():
            old_val = existing.get(key)
            # Special handling for JSONB fields
            if key == "rubric":
                if old_val != new_val:
                    diff[key] = ("...", "...")  # Don't print full rubric
            elif old_val != new_val:
                diff[key] = (old_val, new_val)

        if diff:
            change = ContentChange(
                action="update",
                table="drills",
                identifier=identifier,
                data=drill_data,
                diff=diff,
            )

            if not dry_run:
                client.table("drills").update(drill_data).eq("id", existing["id"]).execute()

            return existing["id"], change
        else:
            return existing["id"], None
    else:
        change = ContentChange(
            action="insert",
            table="drills",
            identifier=identifier,
            data=drill_data,
        )

        if not dry_run:
            response = client.table("drills").insert(drill_data).execute()
            return response.data[0]["id"], change
        else:
            return "DRY_RUN_ID", change


# =============================================================================
# MAIN SEEDING LOGIC
# =============================================================================


def seed_track(
    client: Client, track_dir: Path, dry_run: bool
) -> SeedResult:
    """Seed a single track and all its units and drills."""
    result = SeedResult(changes=[], errors=[])

    # Load and validate track
    track, errors = load_track_content(track_dir)
    result.errors.extend(errors)

    if not track:
        return result

    # Upsert track
    track_id, change = upsert_track(client, track, dry_run)
    if change:
        result.changes.append(change)
    result.tracks_processed += 1

    # Load and process units
    unit_files = discover_units(track_dir)
    unit_id_map: dict[int, str] = {}  # order_index -> unit_id

    for unit_file in unit_files:
        unit, errors = load_unit_content(unit_file)
        result.errors.extend(errors)

        if not unit:
            continue

        if unit.track_slug != track.slug:
            result.errors.append(
                ValidationError_(
                    str(unit_file),
                    "track_slug",
                    f"Unit track_slug '{unit.track_slug}' doesn't match directory track '{track.slug}'",
                )
            )
            continue

        unit_id, change = upsert_unit(client, unit, track_id, dry_run)
        if change:
            result.changes.append(change)
        unit_id_map[unit.order_index] = unit_id
        result.units_processed += 1

    # Load and process drills
    for order_index, unit_id in unit_id_map.items():
        drill_files = discover_drills(track_dir, order_index)
        unit_identifier = f"{track.slug}/unit-{order_index}"

        for drill_file in drill_files:
            drill, errors = load_drill_content(drill_file)
            result.errors.extend(errors)

            if not drill:
                continue

            if drill.unit_order_index != order_index:
                result.errors.append(
                    ValidationError_(
                        str(drill_file),
                        "unit_order_index",
                        f"Drill unit_order_index {drill.unit_order_index} doesn't match directory unit-{order_index}",
                    )
                )
                continue

            _, change = upsert_drill(client, drill, unit_id, unit_identifier, dry_run)
            if change:
                result.changes.append(change)
            result.drills_processed += 1

    return result


def seed_all(client: Client, content_dir: Path, dry_run: bool, track_filter: str | None = None) -> SeedResult:
    """Seed all tracks (or a specific track if filtered)."""
    combined_result = SeedResult(changes=[], errors=[])

    track_dirs = discover_tracks(content_dir)

    if track_filter:
        track_dirs = [d for d in track_dirs if d.name == track_filter]
        if not track_dirs:
            print(f"Error: Track '{track_filter}' not found in {content_dir}")
            sys.exit(1)

    for track_dir in track_dirs:
        print(f"\nProcessing track: {track_dir.name}")
        result = seed_track(client, track_dir, dry_run)

        combined_result.changes.extend(result.changes)
        combined_result.errors.extend(result.errors)
        combined_result.tracks_processed += result.tracks_processed
        combined_result.units_processed += result.units_processed
        combined_result.drills_processed += result.drills_processed

    return combined_result


# =============================================================================
# OUTPUT FORMATTING
# =============================================================================


def print_result(result: SeedResult, dry_run: bool) -> None:
    """Print the seeding result in a clear format."""
    mode = "DRY RUN" if dry_run else "APPLIED"

    print("\n" + "=" * 60)
    print(f"SEED RESULT ({mode})")
    print("=" * 60)

    # Summary
    print(f"\nProcessed: {result.tracks_processed} tracks, {result.units_processed} units, {result.drills_processed} drills")

    # Errors
    if result.errors:
        print(f"\n❌ ERRORS ({len(result.errors)}):")
        for err in result.errors:
            print(f"   {err.file_path}")
            print(f"      Field: {err.field}")
            print(f"      Error: {err.message}")

    # Changes
    if result.changes:
        print(f"\n📝 CHANGES ({len(result.changes)}):")
        for change in result.changes:
            icon = "+" if change.action == "insert" else "~"
            print(f"   {icon} [{change.table}] {change.identifier}")

            if change.diff:
                for field_name, (old, new) in change.diff.items():
                    old_str = str(old)[:50] + "..." if len(str(old)) > 50 else old
                    new_str = str(new)[:50] + "..." if len(str(new)) > 50 else new
                    print(f"      {field_name}: {old_str} → {new_str}")
    else:
        print("\n✅ No changes needed - database is up to date")

    if dry_run and result.changes:
        print("\n⚠️  Run without --dry-run to apply these changes")


# =============================================================================
# CLI
# =============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Seed content from JSON files to Supabase database"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without applying them",
    )
    parser.add_argument(
        "--track",
        type=str,
        help="Seed only a specific track (by directory name)",
    )
    args = parser.parse_args()

    # Find content directory
    try:
        content_dir = find_content_dir()
        print(f"Content directory: {content_dir}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Create Supabase client
    try:
        client = get_supabase_client()
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")
        print("Make sure SUPABASE_URL and SUPABASE_SERVICE_KEY are set in backend/.env")
        sys.exit(1)

    # Run seeding
    result = seed_all(client, content_dir, args.dry_run, args.track)

    # Print result
    print_result(result, args.dry_run)

    # Exit with error code if there were errors
    if result.errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
