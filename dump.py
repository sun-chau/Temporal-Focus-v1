with open("app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt", "r") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    print(f"{i+1:03}: {line}", end="")
