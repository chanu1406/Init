/**
 * Utility Functions
 *
 * Responsibility: General-purpose utility functions.
 * Keep these pure, side-effect free, and well-tested.
 */

/**
 * Combines class names, filtering out falsy values
 * Useful for conditional styling with NativeWind
 *
 * @example
 * cn("text-lg", isActive && "text-blue-500", disabled && "opacity-50")
 */
export function cn(...classes: (string | undefined | null | false)[]): string {
  return classes.filter(Boolean).join(" ");
}

/**
 * Formats a date for display
 * TODO: Implement with proper localization
 */
export function formatDate(date: string | Date): string {
  const d = typeof date === "string" ? new Date(date) : date;
  return d.toLocaleDateString();
}

/**
 * Truncates text to a maximum length
 */
export function truncate(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength - 3) + "...";
}

/**
 * Type-safe delay function
 */
export function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
