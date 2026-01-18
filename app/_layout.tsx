/**
 * Root Layout
 *
 * Responsibility: Provides the root layout wrapper for the entire app.
 * Sets up global providers (QueryClient, etc.) and loads global styles.
 *
 * TODO: Add TanStack Query provider
 * TODO: Add authentication state listener
 * TODO: Add splash screen handling
 */

import "../global.css";
import { Stack } from "expo-router";

export default function RootLayout() {
  // TODO: Initialize QueryClient
  // TODO: Check auth state and redirect accordingly

  return (
    <Stack
      screenOptions={{
        headerShown: false,
      }}
    />
  );
}
