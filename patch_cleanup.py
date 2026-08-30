import re

with open("app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt", "r") as f:
    content = f.read()

# We want only the first JournalEditorScreen. Wait, I should just delete ALL of them and append just one.
# But `JournalEditorScreen` is currently at the end of the file.
# We can find the very first instance of `fun JournalEditorScreen`, delete everything after it (including the function signature), and then append our `JournalEditorScreenExt.kt`.

start_idx = content.find('@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun JournalEditorScreen')

if start_idx != -1:
    content = content[:start_idx]
    
with open("app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt", "w") as f:
    f.write(content)

