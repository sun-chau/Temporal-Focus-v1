with open("app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt", "a") as f:
    with open("JournalEditorScreenExt.kt", "r") as ext:
        content = ext.read()
        start_idx = content.find('@OptIn(ExperimentalMaterial3Api::class)')
        if start_idx != -1:
            f.write("\n" + content[start_idx:])
        
