import re
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

pattern = r"AnimatedVisibility\(\n\s*visible = !isNowLineVisible,"
repl = """AnimatedVisibility(
                    visible = !isNowLineVisible || pagerState.currentPage != (Int.MAX_VALUE / 2),"""
content = re.sub(pattern, repl, content)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
