/**
 * Preferences Store
 *
 * Responsibility: Manages user preferences and app settings.
 * Persisted locally, not synced to server.
 *
 * TODO: Add persistence middleware (AsyncStorage or SecureStore)
 * TODO: Add notification preferences
 * TODO: Add theme preferences
 */

import { create } from "zustand";

interface PreferencesState {
  dailyDrillCount: number;
  notificationsEnabled: boolean;
  preferredTime: string | null; // e.g., "09:00"

  // Actions
  setDailyDrillCount: (count: number) => void;
  setNotificationsEnabled: (enabled: boolean) => void;
  setPreferredTime: (time: string | null) => void;
}

export const usePreferencesStore = create<PreferencesState>((set) => ({
  dailyDrillCount: 3,
  notificationsEnabled: true,
  preferredTime: null,

  setDailyDrillCount: (dailyDrillCount) => set({ dailyDrillCount }),
  setNotificationsEnabled: (notificationsEnabled) =>
    set({ notificationsEnabled }),
  setPreferredTime: (preferredTime) => set({ preferredTime }),
}));
