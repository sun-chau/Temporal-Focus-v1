import re

with open("app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt", "r") as f:
    content = f.read()

content = content.replace('var pin by remember { mutableStateOf("") }', 'var pin by remember { mutableStateOf("") } // it is actually password')
content = content.replace('title = { Text("Enter PIN") }', 'title = { Text("Enter Password") }')
content = content.replace('label = { Text("PIN") }', 'label = { Text("Password") }')
content = content.replace('.setNegativeButtonText("Use PIN")', '.setNegativeButtonText("Use Password")')

with open("app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt", "w") as f:
    f.write(content)

