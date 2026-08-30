with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    text = f.read()

stack = []
for i, c in enumerate(text):
    if c == '{':
        stack.append(text[:i].count(chr(10)) + 1)
    elif c == '}':
        if not stack:
            print(f"Extra closing brace at line {text[:i].count(chr(10)) + 1}")
            break
        stack.pop()
if stack:
    print(f"Missing {len(stack)} closing braces. Unclosed blocks opened at lines: {stack}")
else:
    print("Balanced!")
