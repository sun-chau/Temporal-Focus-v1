import re

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "r") as f:
    content = f.read()

content = content.replace("Icons.Outlined.Notifications", "Icons.Outlined.Alarm")

if "import androidx.compose.material.icons.outlined.Alarm" not in content:
    content = content.replace("import androidx.compose.material.icons.outlined.Notifications", "import androidx.compose.material.icons.outlined.Alarm")

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "w") as f:
    f.write(content)
