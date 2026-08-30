with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

old_click = ".clickable { selectedTag = tag }"
new_click = ".clickable { selectedTag = if (selectedTag == tag) \"\" else tag }"
content = content.replace(old_click, new_click)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
