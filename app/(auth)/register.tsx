/**
 * Register Screen
 *
 * Responsibility: Handles new user registration via Supabase Auth.
 * Contains registration form UI and calls auth service.
 *
 * TODO: Implement registration form UI
 * TODO: Call supabase.auth.signUp
 * TODO: Handle registration errors
 * TODO: Navigate to login or main on success
 */

import { View, Text } from "react-native";

export default function RegisterScreen() {
  // TODO: Add form state with email/password/confirm
  // TODO: Add register handler that calls auth service

  return (
    <View className="flex-1 items-center justify-center p-6">
      <Text className="text-2xl font-bold mb-8">Create Account</Text>
      {/* TODO: Email input */}
      {/* TODO: Password input */}
      {/* TODO: Confirm password input */}
      {/* TODO: Register button */}
      {/* TODO: Link to login */}
    </View>
  );
}
