with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()
line = content[:19651].count('\n') + 1
print(f"Brace closed at line {line}")
