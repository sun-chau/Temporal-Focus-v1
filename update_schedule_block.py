with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

target1 = """                            ScheduleBlock(
                                isWarning = isWarning,"""

replacement1 = """                            val alignTextEnd = durationMinutes < 150 && endMinutes > 22 * 60

                            ScheduleBlock(
                                alignTextEnd = alignTextEnd,
                                isWarning = isWarning,"""

content = content.replace(target1, replacement1)

target2 = """fun ScheduleBlock(
    schedule: DailyScheduleTask,"""

replacement2 = """fun ScheduleBlock(
    alignTextEnd: Boolean = false,
    schedule: DailyScheduleTask,"""

content = content.replace(target2, replacement2)

target3 = """        // Content layer (allowed to bleed horizontally)
        Row(
            modifier = Modifier
                .wrapContentWidth(unbounded = true, align = Alignment.Start)
                .fillMaxHeight()
                .padding(horizontal = 8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {"""

replacement3 = """        // Content layer (allowed to bleed horizontally)
        Row(
            modifier = Modifier
                .wrapContentWidth(unbounded = true, align = if (alignTextEnd) Alignment.End else Alignment.Start)
                .fillMaxHeight()
                .padding(horizontal = 8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {"""

content = content.replace(target3, replacement3)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
