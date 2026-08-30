import re

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

content = content.replace("androidx.compose.foundation.shape.androidx.compose.foundation.shape.RoundedCornerShape", "androidx.compose.foundation.shape.RoundedCornerShape")
content = content.replace("androidx.compose.ui.text.font.androidx.compose.ui.text.font.FontWeight", "androidx.compose.ui.text.font.FontWeight")

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)
