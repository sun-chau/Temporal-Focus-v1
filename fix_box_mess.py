import re
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

pattern = r"    Box\(\n        modifier = modifier\n    \) \{\n        // Colored background layer \(strictly constrained to blockWidth\)\n        val shape = RoundedCornerShape\(\n            topStart = if \(isBleedLeft\) 0\.dp else 8\.dp,\n            bottomStart = if \(isBleedLeft\) 0\.dp else 8\.dp,\n            topEnd = if \(isBleedRight\) 0\.dp else 8\.dp,\n            bottomEnd = if \(isBleedRight\) 0\.dp else 8\.dp\n    \)\n    Box\(\n        modifier = modifier\.shadow\(elevation, shape, clip = false\)\n    \) \{\n        // Colored background layer \(strictly constrained to blockWidth\)"

replacement = """    val shape = RoundedCornerShape(
        topStart = if (isBleedLeft) 0.dp else 8.dp,
        bottomStart = if (isBleedLeft) 0.dp else 8.dp,
        topEnd = if (isBleedRight) 0.dp else 8.dp,
        bottomEnd = if (isBleedRight) 0.dp else 8.dp
    )
    Box(
        modifier = modifier.shadow(elevation, shape, clip = false)
    ) {"""

content = re.sub(pattern, replacement, content)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
