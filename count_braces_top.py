with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    lines = f.readlines()

depth = 0
for i, line in enumerate(lines):
    depth += line.count('{')
    depth -= line.count('}')
    if "Scaffold(" in line or "Column(" in line or "HorizontalPager(" in line:
        print(f"Line {i+1} depth: {depth} | {line.strip()}")
