import sys

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# I need to add nestedScroll modifier to the parent Box.
# First, let's create the NestedScrollConnection right before the Box.
# Find:
#            val threshold = 150f
#
#            Box(
#                modifier = Modifier
#                    .weight(1f)
#                    .fillMaxWidth()
#            ) {

target = """            val threshold = 150f
            
            Box(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
            ) {"""

# wait, I should make sure the target matches perfectly.
# let's just use re.sub for robust matching.

import re

pattern = r'val threshold = 150f\s*Box\(\s*modifier = Modifier\s*\.weight\(1f\)\s*\.fillMaxWidth\(\)\s*\) \{'

replacement = """val threshold = 150f
            
            val nestedScrollConnection = remember {
                object : androidx.compose.ui.input.nestedscroll.NestedScrollConnection {
                    override fun onPostScroll(
                        consumed: androidx.compose.ui.geometry.Offset,
                        available: androidx.compose.ui.geometry.Offset,
                        source: androidx.compose.ui.input.nestedscroll.NestedScrollSource
                    ): androidx.compose.ui.geometry.Offset {
                        if (available.x != 0f) {
                            overscrollOffset += available.x * 0.3f
                            
                            if (kotlin.math.abs(overscrollOffset) >= threshold && !hasVibrated) {
                                haptic.performHapticFeedback(androidx.compose.ui.hapticfeedback.HapticFeedbackType.LongPress)
                                hasVibrated = true
                            } else if (kotlin.math.abs(overscrollOffset) < threshold) {
                                hasVibrated = false
                            }
                        }
                        return super.onPostScroll(consumed, available, source)
                    }

                    override suspend fun onPreFling(available: androidx.compose.ui.unit.Velocity): androidx.compose.ui.unit.Velocity {
                        if (overscrollOffset > threshold) {
                            selectedDateMillis -= 24 * 60 * 60 * 1000L
                        } else if (overscrollOffset < -threshold) {
                            selectedDateMillis += 24 * 60 * 60 * 1000L
                        }
                        overscrollOffset = 0f
                        hasVibrated = false
                        return super.onPreFling(available)
                    }
                }
            }

            Box(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                    .androidx.compose.ui.input.nestedscroll.nestedScroll(nestedScrollConnection)
            ) {"""

if not re.search(pattern, content):
    print("Could not find the target pattern")
    sys.exit(1)

content = re.sub(pattern, replacement, content)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
print("Updated NestedScrollConnection")
