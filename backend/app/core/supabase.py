"""
Supabase Client

Responsibility: Provides Supabase client instances for database operations.
"""

from supabase import create_client, Client
from app.core.config import settings


def get_supabase_client() -> Client:
    """
    Dependency for getting a Supabase client.
    
    Uses the service role key for backend operations.
    This bypasses RLS policies - use with caution.
    """
    return create_client(settings.supabase_url, settings.supabase_service_key)
