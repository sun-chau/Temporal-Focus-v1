import re

with open("app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt", "r") as f:
    content = f.read()

content = content.replace("FloatingActionButton(onClick = { showTemplateSelectionSheet = true }) {", 
"FloatingActionButton(onClick = { showTemplateSelectionSheet = true }, containerColor = MaterialTheme.colorScheme.primary, contentColor = MaterialTheme.colorScheme.background) {")

content = content.replace("FloatingActionButton(onClick = { creatingTemplate = true }) {",
"FloatingActionButton(onClick = { creatingTemplate = true }, containerColor = MaterialTheme.colorScheme.primary, contentColor = MaterialTheme.colorScheme.background) {")

with open("app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt", "w") as f:
    f.write(content)
