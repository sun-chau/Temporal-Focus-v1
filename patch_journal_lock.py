import re

with open("app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt", "r") as f:
    content = f.read()

content = content.replace("    if (!isUnlocked) {", "    if (!isUnlocked && uiState.privateJournalLockEnabled) {")

with open("app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt", "w") as f:
    f.write(content)

