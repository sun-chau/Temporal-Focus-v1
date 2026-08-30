with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    lines = f.readlines()

nesting = 0
for i, line in enumerate(lines):
    nesting += line.count('{')
    nesting -= line.count('}')
    if nesting < 0:
        print(f"Error: nesting < 0 at line {i+1}")
        break

print(f"Final nesting: {nesting}")
