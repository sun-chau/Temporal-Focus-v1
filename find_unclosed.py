with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    lines = f.readlines()

stack = []
for i, line in enumerate(lines):
    for j, char in enumerate(line):
        if char == '{':
            stack.append((i + 1, line.strip()))
        elif char == '}':
            if stack:
                stack.pop()

for item in stack:
    print(f"Line {item[0]}: {item[1]}")
