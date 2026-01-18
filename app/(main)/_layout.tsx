/**
 * Main App Layout
 *
 * Responsibility: Layout wrapper for authenticated app screens.
 * Ensures only authenticated users can access these routes.
 *
 * TODO: Redirect unauthenticated users to /(auth)/login
 * TODO: Set up tab or stack navigation for main app flow
 */

import { Stack } from "expo-router";

export default function MainLayout() {
  // TODO: Check if user is authenticated, redirect to /(auth)/login if not

  return (
    <Stack
      screenOptions={{
        headerShown: true,
      }}
    />
  );
}
