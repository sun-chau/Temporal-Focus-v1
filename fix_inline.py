import re

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'r') as f:
    content = f.read()

regex = r"            // Setup Phase Settings \(Only active when stopped\)\s+if \(!uiState\.hasPomodoroStarted\) \{.*?\} else \{\s+// Live modifier when running"

replacement = r"""            // Live modifier when running (only active when started)
            if (uiState.hasPomodoroStarted) {
                 // Live modifier when running"""

new_content = re.sub(regex, replacement, content, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'w') as f:
    f.write(new_content)

