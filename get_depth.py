with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    lines = f.readlines()

depth = 0
for i, line in enumerate(lines[:384]):
    depth += line.count('{') - line.count('}')
    
print(f"Depth at line 384: {depth}")
