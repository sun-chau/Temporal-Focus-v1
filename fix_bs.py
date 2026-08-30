import re

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'r') as f:
    content = f.read()

# 1. Un-nest the settings gear
gear_regex = r"if \(!uiState\.hasPomodoroStarted\) \{\s*(IconButton\(onClick = \{ showSettingsDialog = true \}.*?tint = MaterialTheme\.colorScheme\.onSurface\s*\)\s*\}\s*)\}"
content = re.sub(gear_regex, r"\1", content, flags=re.DOTALL)

# 2. Fix ModalBottomSheet
# Replace the old `if (showSettingsDialog && !uiState.hasPomodoroStarted)` block
import textwrap

bs_start = content.find("if (showSettingsDialog && !uiState.hasPomodoroStarted) {")
if bs_start != -1:
    # Need to find the end of this block. We'll just replace everything from bs_start up to the @Composable of PomodoroStatCard
    bs_end = content.find("@Composable\nfun PomodoroStatCard", bs_start)
    if bs_end != -1:
        # But wait, there is the Stats sheet logic inside PomodoroScreen as well.
        # "if (showStats) {" is earlier or later?
        pass

