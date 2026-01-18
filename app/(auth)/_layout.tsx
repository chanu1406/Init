/**
 * Auth Layout
 *
 * Responsibility: Layout wrapper for authentication screens (login, register).
 * Ensures unauthenticated users stay within auth flow.
 *
 * TODO: Redirect authenticated users away from auth screens
 */

import { Stack } from "expo-router";

export default function AuthLayout() {
  // TODO: Check if user is already authenticated, redirect to /(main)

  return (
    <Stack
      screenOptions={{
        headerShown: false,
      }}
    />
  );
}
