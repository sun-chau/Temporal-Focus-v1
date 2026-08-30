with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    lines = f.readlines()

# find line 389
for i in range(max(0, 389 - 15), min(len(lines), 389 + 5)):
    print(f"{i+1}: {lines[i].rstrip()}")

