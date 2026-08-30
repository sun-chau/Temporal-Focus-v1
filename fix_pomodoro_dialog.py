path = 'app/src/main/java/com/example/ui/screens/PomodoroScreen.kt'
with open(path, 'r') as f:
    content = f.read()

import re
# Remove the Reset Data button in PomodoroStatsDialog
button_pattern = r'''\s*Button\(\s*onClick = \{ showResetDialog = true \},\s*colors = ButtonDefaults\.buttonColors\(\s*containerColor = MaterialTheme\.colorScheme\.errorContainer,\s*contentColor = MaterialTheme\.colorScheme\.onErrorContainer\s*\),\s*modifier = Modifier\.fillMaxWidth\(\)\s*\) \{\s*Text\("Hard Reset Data"\)\s*\}'''

content = re.sub(button_pattern, '', content)

with open(path, 'w') as f:
    f.write(content)

print("Removed hard reset button from dialog.")
