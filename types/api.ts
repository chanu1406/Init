/**
 * API Types
 *
 * Responsibility: Request and response types for API communication.
 * These match the backend schemas.
 */

import type { AIFeedback, Drill } from "./domain";

/**
 * Submit drill response request
 */
export interface SubmitDrillRequest {
  drillId: string;
  response: string;
}

/**
 * Submit drill response result
 */
export interface SubmitDrillResponse {
  attemptId: string;
  feedback: AIFeedback;
  newMasteryScore: number;
  nextReviewDueAt: string;
}

/**
 * Get today's drill response
 */
export interface TodayDrillResponse {
  drill: Drill | null;
  remainingCount: number;
  completedToday: number;
}

/**
 * Generic API error response
 */
export interface ApiError {
  detail: string;
  code?: string;
}
