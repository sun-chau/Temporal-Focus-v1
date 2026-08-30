with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

target = """        // Content layer (allowed to bleed horizontally)
        Row(
            modifier = Modifier
                .wrapContentWidth(unbounded = true, align = if (alignTextEnd) Alignment.End else Alignment.Start)
                .fillMaxHeight()
                .padding(horizontal = 8.dp),"""

replacement = """        // Content layer (allowed to bleed horizontally)
        Row(
            modifier = Modifier
                .width(blockWidth)
                .wrapContentWidth(unbounded = true, align = if (alignTextEnd) Alignment.End else Alignment.Start)
                .fillMaxHeight()
                .padding(horizontal = 8.dp),"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
        f.write(content)
    print("Success")
else:
    print("Target not found")
