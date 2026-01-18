/**
 * App Configuration Constants
 *
 * Responsibility: Centralized app configuration values.
 * Avoid magic numbers in code; define them here.
 */

/**
 * Mastery score range
 */
export const MASTERY = {
  MIN: 0,
  MAX: 5,
  THRESHOLD_MASTERED: 4,
} as const;

/**
 * Drill difficulty range
 */
export const DIFFICULTY = {
  MIN: 1,
  MAX: 5,
} as const;

/**
 * Default daily settings
 */
export const DEFAULTS = {
  DAILY_DRILL_COUNT: 3,
  PREFERRED_TIME: "09:00",
} as const;

/**
 * Spaced repetition intervals (in days)
 * Based on simplified SM-2 algorithm
 */
export const SPACED_REPETITION = {
  INTERVALS: [1, 3, 7, 14, 30, 60] as const,
} as const;

/**
 * API endpoints
 */
export const ENDPOINTS = {
  HEALTH: "/health",
  DRILLS: "/drills",
  PROGRESS: "/progress",
  TRACKS: "/tracks",
} as const;
