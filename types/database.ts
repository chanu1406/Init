/**
 * Database Types (Supabase Generated)
 *
 * Responsibility: TypeScript types generated from Supabase schema.
 * These should be regenerated when the database schema changes.
 *
 * TODO: Generate this file using `supabase gen types typescript`
 */

export interface Database {
  public: {
    Tables: {
      tracks: {
        Row: {
          id: string;
          slug: string;
          title: string;
          description: string;
          created_at: string;
        };
        Insert: {
          id?: string;
          slug: string;
          title: string;
          description: string;
          created_at?: string;
        };
        Update: {
          id?: string;
          slug?: string;
          title?: string;
          description?: string;
          created_at?: string;
        };
      };
      units: {
        Row: {
          id: string;
          track_id: string;
          order_index: number;
          summary_markdown: string;
        };
        Insert: {
          id?: string;
          track_id: string;
          order_index: number;
          summary_markdown: string;
        };
        Update: {
          id?: string;
          track_id?: string;
          order_index?: number;
          summary_markdown?: string;
        };
      };
      drills: {
        Row: {
          id: string;
          unit_id: string;
          drill_type: "quiz" | "explain" | "debug";
          prompt_markdown: string;
          rubric: Record<string, unknown>;
          difficulty: number;
          estimated_minutes: number;
          concept_tags: string[];
        };
        Insert: {
          id?: string;
          unit_id: string;
          drill_type: "quiz" | "explain" | "debug";
          prompt_markdown: string;
          rubric: Record<string, unknown>;
          difficulty: number;
          estimated_minutes: number;
          concept_tags?: string[];
        };
        Update: {
          id?: string;
          unit_id?: string;
          drill_type?: "quiz" | "explain" | "debug";
          prompt_markdown?: string;
          rubric?: Record<string, unknown>;
          difficulty?: number;
          estimated_minutes?: number;
          concept_tags?: string[];
        };
      };
      user_drill_progress: {
        Row: {
          id: string;
          user_id: string;
          drill_id: string;
          mastery_score: number;
          last_attempt_at: string;
          next_review_due_at: string;
        };
        Insert: {
          id?: string;
          user_id: string;
          drill_id: string;
          mastery_score: number;
          last_attempt_at?: string;
          next_review_due_at: string;
        };
        Update: {
          id?: string;
          user_id?: string;
          drill_id?: string;
          mastery_score?: number;
          last_attempt_at?: string;
          next_review_due_at?: string;
        };
      };
      drill_attempts: {
        Row: {
          id: string;
          user_id: string;
          drill_id: string;
          user_response: string;
          ai_feedback: Record<string, unknown>;
          created_at: string;
        };
        Insert: {
          id?: string;
          user_id: string;
          drill_id: string;
          user_response: string;
          ai_feedback: Record<string, unknown>;
          created_at?: string;
        };
        Update: {
          id?: string;
          user_id?: string;
          drill_id?: string;
          user_response?: string;
          ai_feedback?: Record<string, unknown>;
          created_at?: string;
        };
      };
    };
    Views: Record<string, never>;
    Functions: Record<string, never>;
    Enums: {
      drill_type: "quiz" | "explain" | "debug";
    };
  };
}
