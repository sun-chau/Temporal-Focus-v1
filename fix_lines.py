with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    lines = f.readlines()

# The pointerInput block ended around 256.
# 257 is: } else if (delta < 0 && !horizontalScrollState.canScrollForward) {
# We want to remove lines 257 to 291 inclusive.
# 0-indexed: 256 to 290.

new_lines = lines[:256] + lines[291:]

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.writelines(new_lines)
    
print("Removed garbage")
