/**
 * Home Screen (Main)
 *
 * Responsibility: Primary authenticated home screen.
 * Shows daily drill, progress summary, and navigation to tracks.
 *
 * TODO: Display today's drill or call-to-action
 * TODO: Show mastery progress summary
 * TODO: Navigate to drill detail or tracks list
 */

import { View, Text } from "react-native";

export default function HomeScreen() {
  // TODO: Fetch today's scheduled drill from API
  // TODO: Display user progress stats

  return (
    <View className="flex-1 p-6">
      <Text className="text-2xl font-bold mb-4">Today's Practice</Text>
      {/* TODO: Daily drill card */}
      {/* TODO: Progress summary */}
      {/* TODO: Quick actions */}
    </View>
  );
}
