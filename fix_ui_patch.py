with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

old_text = """                Text(
                    text = getTagName(schedule.tag), 
                    fontSize = 12.sp, 
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    softWrap = false
                )"""

new_text = """                if (schedule.tag.isNotBlank()) {
                    Text(
                        text = getTagName(schedule.tag), 
                        fontSize = 12.sp, 
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 1,
                        softWrap = false
                    )
                }"""

content = content.replace(old_text, new_text)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
