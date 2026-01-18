/**
 * App Entry Point
 *
 * Responsibility: Initial screen shown when app loads.
 * Redirects to auth or main flow based on authentication state.
 *
 * TODO: Implement auth check and redirect logic
 * TODO: Add loading state while checking auth
 */

import { View, Text } from "react-native";

export default function Index() {
  // TODO: Check auth state and redirect to /(auth)/login or /(main)

  return (
    <View className="flex-1 items-center justify-center">
      <Text className="text-lg">Init</Text>
    </View>
  );
}
