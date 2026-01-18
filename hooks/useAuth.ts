/**
 * useAuth Hook
 *
 * Responsibility: Provides authentication actions and state.
 * Wraps Supabase Auth methods and integrates with session store.
 *
 * TODO: Implement signIn method
 * TODO: Implement signUp method
 * TODO: Implement signOut method
 * TODO: Add auth state listener on mount
 */

import { useSessionStore } from "@/store/session";

export function useAuth() {
  const { user, isAuthenticated, isLoading, setUser, clearSession } =
    useSessionStore();

  /**
   * Sign in with email and password
   * TODO: Implement with Supabase Auth
   */
  const signIn = async (email: string, password: string) => {
    // TODO: Call supabase.auth.signInWithPassword
    // TODO: Update session store on success
    // TODO: Handle errors
    throw new Error("Not implemented");
  };

  /**
   * Register new user with email and password
   * TODO: Implement with Supabase Auth
   */
  const signUp = async (email: string, password: string) => {
    // TODO: Call supabase.auth.signUp
    // TODO: Handle email verification if required
    // TODO: Handle errors
    throw new Error("Not implemented");
  };

  /**
   * Sign out current user
   * TODO: Implement with Supabase Auth
   */
  const signOut = async () => {
    // TODO: Call supabase.auth.signOut
    // TODO: Clear session store
    clearSession();
  };

  return {
    user,
    isAuthenticated,
    isLoading,
    signIn,
    signUp,
    signOut,
  };
}
