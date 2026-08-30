import re

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'r') as f:
    content = f.read()

# Remove LiveAdjustmentButton
content = re.sub(r'@Composable\nfun LiveAdjustmentButton\(.*?\}\n\}', '', content, flags=re.DOTALL)

# Remove PomodoroArcDial
content = re.sub(r'@Composable\nprivate fun PomodoroArcDial\(.*?\}\n\}', '', content, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'w') as f:
    f.write(content)
