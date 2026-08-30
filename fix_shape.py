import re
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

if "import androidx.compose.ui.draw.shadow" not in content:
    content = content.replace("import androidx.compose.ui.draw.clip", "import androidx.compose.ui.draw.clip\nimport androidx.compose.ui.draw.shadow")

shape_pattern = r"    Box\(\n        modifier = modifier\.shadow\(elevation, shape, clip = false\)\n    \) \{\n        // Colored background layer \(strictly constrained to blockWidth\)\n        val shape = RoundedCornerShape\("

shape_replacement = """    val shape = RoundedCornerShape(
        topStart = if (isBleedLeft) 0.dp else 8.dp,
        bottomStart = if (isBleedLeft) 0.dp else 8.dp,
        topEnd = if (isBleedRight) 0.dp else 8.dp,
        bottomEnd = if (isBleedRight) 0.dp else 8.dp
    )
    Box(
        modifier = modifier.shadow(elevation, shape, clip = false)
    ) {
        // Colored background layer (strictly constrained to blockWidth)
        """

# But my previous script replaced `modifier = modifier` with `modifier = modifier.shadow(...)`
# Let's see the exact text:
content = content.replace("    Box(\n        modifier = modifier.shadow(elevation, shape, clip = false)\n    ) {\n        // Colored background layer (strictly constrained to blockWidth)\n        val shape = RoundedCornerShape(", "    val shape = RoundedCornerShape(")
content = content.replace("bottomEnd = if (isBleedRight) 0.dp else 8.dp\n        )", "bottomEnd = if (isBleedRight) 0.dp else 8.dp\n    )\n    Box(\n        modifier = modifier.shadow(elevation, shape, clip = false)\n    ) {\n        // Colored background layer (strictly constrained to blockWidth)")

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
