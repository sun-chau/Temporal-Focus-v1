with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    lines = f.readlines()

nesting = 0
for i, line in enumerate(lines[:340]):
    open_count = line.count('{')
    close_count = line.count('}')
    nesting += open_count - close_count
    
    if open_count > 0 or close_count > 0:
        print(f"{i+1} [{nesting}]: {line.strip()}")
