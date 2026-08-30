import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# 1. Remove overscroll variables
pattern_vars = r'\s*var overscrollOffset by remember \{ mutableStateOf\(0f\) \}\n\s*val density = androidx\.compose\.ui\.platform\.LocalDensity\.current\n\s*val activationThreshold = with\(density\) \{ 50\.dp\.toPx\(\) \}\n\s*val isThresholdCrossed by remember \{ androidx\.compose\.runtime\.derivedStateOf \{ kotlin\.math\.abs\(overscrollOffset\) >= activationThreshold \} \}\n\s*val haptic = androidx\.compose\.ui\.platform\.LocalHapticFeedback\.current\n\s*val coroutineScope = rememberCoroutineScope\(\)\n'
content = re.sub(pattern_vars, '\n', content)

# 2. Remove the peek UI Box
# We know it starts with `// Add visual overscroll indicator` and ends before `androidx.compose.runtime.CompositionLocalProvider`
pattern_peek = r'\s*// Add visual overscroll indicator \(The Peek UI\).*?if \(overscrollOffset != 0f\) \{.*?\}\n\s*\}\n'
content = re.sub(pattern_peek, '\n', content, flags=re.DOTALL)

# 3. Remove the pointerInput and offset modifiers
pattern_modifiers = r'\s*\.offset \{ androidx\.compose\.ui\.unit\.IntOffset\(overscrollOffset\.toInt\(\), 0\) \}\n\s*\.horizontalScroll\(horizontalScrollState\)\n\s*\.pointerInput\(horizontalScrollState\.canScrollForward, horizontalScrollState\.canScrollBackward\) \{.*?\n\s*\}'
content = re.sub(pattern_modifiers, '\n                        .horizontalScroll(horizontalScrollState)', content, flags=re.DOTALL)

# 4. Remove the CompositionLocalProvider
# We need to remove: `androidx.compose.runtime.CompositionLocalProvider(androidx.compose.foundation.LocalOverscrollConfiguration provides null) {`
# and one closing brace at the end of the `Box` containing the `Column`.
content = content.replace("androidx.compose.runtime.CompositionLocalProvider(androidx.compose.foundation.LocalOverscrollConfiguration provides null) {\n", "")

# We have one extra closing brace to remove. Let's check the end of the DailyScheduleScreen function.
