with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    lines = f.readlines()

stack = []
for i in range(830, 1050):
    line = lines[i]
    for j, char in enumerate(line):
        if char == '{':
            stack.append((i + 1, line.strip()))
        elif char == '}':
            if stack:
                stack.pop()
            else:
                print(f"Extra closing brace at line {i + 1}")

print(f"Net open braces inside block: {len(stack)}")
for item in stack:
    print(f"Unclosed: Line {item[0]}: {item[1]}")
