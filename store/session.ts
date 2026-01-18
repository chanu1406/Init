/**
 * Session Store
 *
 * Responsibility: Manages user session state (auth, user profile).
 * Uses Zustand for local state management.
 *
 * NOTE: Server state (drills, progress) should use TanStack Query, not Zustand.
 *
 * TODO: Integrate with Supabase Auth state listener
 * TODO: Add user profile data
 */

import { create } from "zustand";
import type { User } from "@/types/domain";

interface SessionState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;

  // Actions
  setUser: (user: User | null) => void;
  setLoading: (loading: boolean) => void;
  clearSession: () => void;
}

export const useSessionStore = create<SessionState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,

  setUser: (user) =>
    set({
      user,
      isAuthenticated: user !== null,
      isLoading: false,
    }),

  setLoading: (isLoading) => set({ isLoading }),

  clearSession: () =>
    set({
      user: null,
      isAuthenticated: false,
      isLoading: false,
    }),
}));
