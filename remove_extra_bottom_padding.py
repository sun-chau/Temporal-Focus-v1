import os

files = [
    'app/src/main/java/com/example/ui/screens/SettingsScreen.kt',
    'app/src/main/java/com/example/ui/screens/UserAccountScreen.kt'
]

for path in files:
    with open(path, 'r') as f:
        content = f.read()
    
    content = content.replace(
        "Spacer(modifier = Modifier.height(WindowInsets.navigationBars.asPaddingValues().calculateBottomPadding()))",
        ""
    )
    
    with open(path, 'w') as f:
        f.write(content)
