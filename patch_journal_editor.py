import re

with open("app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt", "r") as f:
    content = f.read()

start_idx = content.find('@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun JournalEditorScreen')
end_idx = content.find('@Composable\nfun JournalEntryCard(', start_idx)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + content[end_idx:]

with open("app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt", "w") as f:
    f.write(content)

