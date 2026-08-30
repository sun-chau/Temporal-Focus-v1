with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    lines = f.readlines()

depth = 0
for i, line in enumerate(lines):
    depth += line.count('{') - line.count('}')
    if depth < 0:
        print(f"Depth became negative at line {i+1}: {line.strip()}")
        break
