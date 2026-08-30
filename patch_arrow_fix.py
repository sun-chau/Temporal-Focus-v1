import re

with open("app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt", "r") as f:
    content = f.read()

content = content.replace("androidx.compose.material.icons.Icons.AutoMirrored.Filled.ArrowBack", "androidx.compose.material.icons.automirrored.filled.ArrowBack")
content = content.replace("import androidx.compose.material.icons.automirrored.filled.ArrowBack", "import androidx.compose.material.icons.automirrored.filled.ArrowBack")

with open("app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt", "w") as f:
    f.write(content)

