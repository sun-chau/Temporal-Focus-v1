with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    lines = f.readlines()

nesting = 0
for i, line in enumerate(lines):
    open_count = line.count('{')
    close_count = line.count('}')
    nesting += open_count - close_count
    
    # print every 50 lines to see where nesting drops
    if i % 50 == 0:
        print(f"Line {i}: nesting = {nesting}")
    if nesting < 0:
        print(f"Error at line {i+1}")
        break
