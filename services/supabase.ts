/**
 * Supabase Client
 *
 * Responsibility: Initializes and exports the Supabase client instance.
 * Used for authentication and database operations from the frontend.
 *
 * TODO: Configure secure storage for auth tokens (expo-secure-store)
 */

import { createClient } from "@supabase/supabase-js";
import type { Database } from "@/types/database";

const supabaseUrl = process.env.EXPO_PUBLIC_SUPABASE_URL!;
const supabaseAnonKey = process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY!;

// TODO: Add custom storage adapter using expo-secure-store for auth persistence
// TODO: Add error handling for missing environment variables

export const supabase = createClient<Database>(supabaseUrl, supabaseAnonKey, {
  auth: {
    // TODO: Configure auth storage with SecureStore
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: false,
  },
});
