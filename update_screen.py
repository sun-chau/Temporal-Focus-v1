import re

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'r') as f:
    content = f.read()

# 1. Update Gear Icon in Top App Bar
# Currently it might be wrapped in if (showSettingsDialog && !uiState.hasPomodoroStarted) but actually in the TopAppBar it was:
# if (!uiState.hasPomodoroStarted) { IconButton(...) { Icon(...) } }
content = re.sub(r'if \(!uiState\.hasPomodoroStarted\) \{\s*IconButton\(onClick = \{ showSettingsDialog = true \}.*?\)\s*\{\s*Icon\(Icons\.Default\.Settings.*?\)\s*\}\s*\}',
                 r'IconButton(onClick = { showSettingsDialog = true }, modifier = Modifier.offset(x = 12.dp)) { Icon(Icons.Default.Settings, contentDescription = "Settings", tint = MaterialTheme.colorScheme.onSurface) }',
                 content, flags=re.DOTALL)

# 2. Change timer text from 110.sp to 120.sp
content = content.replace("fontSize = 110.sp,", "fontSize = 120.sp,")

# 3. Modify drag gesture 
# In the original, it was `if (!uiState.isPomodoroRunning && !uiState.hasPomodoroStarted)`
# We need to change to just `if (!uiState.hasPomodoroStarted)`
content = re.sub(
    r'if \(!uiState\.isPomodoroRunning && !uiState\.hasPomodoroStarted\) \{.*?\} else \{.*?\}',
    r'''if (!uiState.hasPomodoroStarted) {
                                                when (uiState.currentPhase) {
                                                    PomodoroPhase.FOCUS -> viewModel.adjustBaseFocusTime(minutesDelta)
                                                    PomodoroPhase.BREAK -> viewModel.adjustBaseBreakTime(minutesDelta)
                                                    PomodoroPhase.LONG_BREAK -> viewModel.adjustLongBreakTime(minutesDelta)
                                                }
                                            }''',
    content, flags=re.DOTALL
)

# 4. Modify Bottom Sheet 
# Need to replace the whole `if (showSettingsDialog && !uiState.hasPomodoroStarted) { ModalBottomSheet(...) ... }`
# with the new logic.

# find the start of ModalBottomSheet block
# "if (showSettingsDialog"
import sys
# It's better to just rewrite the ModalBottomSheet piece dynamically.
