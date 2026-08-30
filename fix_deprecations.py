import sys

with open("app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt", "r") as f:
    content = f.read()

content = content.replace("Icons.Filled.ArrowBack", "Icons.AutoMirrored.Filled.ArrowBack")
content = content.replace("Divider(modifier = Modifier", "androidx.compose.material3.HorizontalDivider(modifier = Modifier")

with open("app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt", "w") as f:
    f.write(content)

