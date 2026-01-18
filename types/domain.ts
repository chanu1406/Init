/**
 * Domain Types
 *
 * Responsibility: Core domain entity types used throughout the app.
 * These map to database tables and business concepts.
 *
 * NOTE: Keep in sync with backend models and database schema.
 */

/**
 * User entity
 */
export interface User {
  id: string;
  email: string;
  createdAt: string;
}

/**
 * Track - High-level learning path
 * Example: "systems-101", "devops-basics"
 */
export interface Track {
  id: string;
  slug: string;
  title: string;
  description: string;
  createdAt: string;
}

/**
 * Unit - Ordered section within a track
 */
export interface Unit {
  id: string;
  trackId: string;
  orderIndex: number;
  summaryMarkdown: string;
}

/**
 * Drill types supported by the system
 */
export type DrillType = "quiz" | "explain" | "debug";

/**
 * Drill - Atomic learning action
 */
export interface Drill {
  id: string;
  unitId: string;
  drillType: DrillType;
  promptMarkdown: string;
  rubric: DrillRubric;
  difficulty: number; // 1-5
  estimatedMinutes: number;
  conceptTags: string[];
}

/**
 * Rubric for grading drill responses
 */
export interface DrillRubric {
  criteria: RubricCriterion[];
  expectedKeyPoints: string[];
  commonMistakes: string[];
}

export interface RubricCriterion {
  name: string;
  description: string;
  maxScore: number;
}

/**
 * User's progress on a specific drill
 */
export interface UserDrillProgress {
  id: string;
  userId: string;
  drillId: string;
  masteryScore: number; // 0-5
  lastAttemptAt: string;
  nextReviewDueAt: string;
}

/**
 * Individual drill attempt record
 */
export interface DrillAttempt {
  id: string;
  userId: string;
  drillId: string;
  userResponse: string;
  aiFeedback: AIFeedback;
  createdAt: string;
}

/**
 * AI grading feedback structure
 */
export interface AIFeedback {
  scores: CriterionScore[];
  totalScore: number;
  maxScore: number;
  justification: string;
  improvement: string;
  followUpQuestion?: string;
}

export interface CriterionScore {
  criterion: string;
  score: number;
  maxScore: number;
  feedback: string;
}
