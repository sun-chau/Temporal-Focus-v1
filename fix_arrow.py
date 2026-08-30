import re

with open("app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt", "r") as f:
    content = f.read()

# Replace any incorrect ArrowBack usages
content = content.replace("androidx.compose.material.icons.automirrored.filled.ArrowBack", "Icons.AutoMirrored.Filled.ArrowBack")

# Fix the import
content = content.replace("import Icons.AutoMirrored.Filled.ArrowBack", "import androidx.compose.material.icons.automirrored.filled.ArrowBack")

with open("app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt", "w") as f:
    f.write(content)

