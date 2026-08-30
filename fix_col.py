import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Replace the Column modifiers
pattern = r'(Column\(\s*modifier = Modifier\s*\.fillMaxSize\(\)\s*\.offset \{ androidx\.compose\.ui\.unit\.IntOffset\(overscrollOffset\.toInt\(\), 0\) \})'
replacement = r'\1\n                        .horizontalScroll(horizontalScrollState)'

content = re.sub(pattern, replacement, content)

# Remove the wrapper Box around BoxWithConstraints in Canvas Body
# Let's just remove the empty Box() {} that I added earlier.
box_pattern = r'Box\(\s*modifier = Modifier\s*\.fillMaxSize\(\)\s*\) \{\s*(androidx\.compose\.foundation\.layout\.BoxWithConstraints)'
box_replacement = r'\1'
content = re.sub(box_pattern, box_replacement, content)

# And remove one closing brace before "if (reschedulingSchedule != null) {"
brace_pattern = r'\}\s*\}\s*\}\s*\}\s*\}\s*\}\s*\}\s*if \(reschedulingSchedule != null\)'
brace_replacement = r'}\n            }\n        }\n    }\n    \n    if (reschedulingSchedule != null)'
content = re.sub(brace_pattern, brace_replacement, content)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)

