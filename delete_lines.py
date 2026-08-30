with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    lines = f.readlines()

def should_delete(idx):
    line_num = idx + 1
    if 151 <= line_num <= 157: return True
    if 165 <= line_num <= 194: return True
    if line_num == 197: return True
    if line_num == 201: return True
    if 203 <= line_num <= 256: return True
    # wait, the pointerInput block closed at 256? Let me check line 257 in the previous output.
    # Ah, in previous output 256 was "                            }", 257 was "                        }"
    if line_num == 257: return True
    return False

new_lines = []
for i, line in enumerate(lines):
    if not should_delete(i):
        new_lines.append(line)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.writelines(new_lines)
