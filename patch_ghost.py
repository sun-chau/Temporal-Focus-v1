import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

target_ghost = """                                    .clip(RoundedCornerShape(8.dp))
                                    .background(bgColor)
                                    .drawBehind {
                                        val stroke = androidx.compose.ui.graphics.drawscope.Stroke(
                                            width = 2.dp.toPx(),
                                            pathEffect = androidx.compose.ui.graphics.PathEffect.dashPathEffect(floatArrayOf(10f, 10f), 0f)
                                        )
                                        drawRoundRect(
                                            color = borderColor,
                                            style = stroke,
                                            cornerRadius = androidx.compose.ui.geometry.CornerRadius(8.dp.toPx(), 8.dp.toPx())
                                        )
                                    }"""

replacement_ghost = """                                    .clip(RectangleShape)
                                    .background(bgColor)
                                    .drawBehind {
                                        val stroke = androidx.compose.ui.graphics.drawscope.Stroke(
                                            width = 2.dp.toPx(),
                                            pathEffect = androidx.compose.ui.graphics.PathEffect.dashPathEffect(floatArrayOf(10f, 10f), 0f)
                                        )
                                        drawRect(
                                            color = borderColor,
                                            style = stroke
                                        )
                                    }"""

content = content.replace(target_ghost, replacement_ghost)

# Floating text for ghost block
target_ghost_text = """                            Box(
                                modifier = Modifier
                                    .offset(x = ghostXOffset, y = ghostYOffset - 24.dp)
                                    .background(borderColor, RoundedCornerShape(4.dp))
                                    .padding(horizontal = 6.dp, vertical = 2.dp)
                            ) {
                                Text(
                                    text = "$startStr - $endStr",
                                    color = MaterialTheme.colorScheme.onPrimary,
                                    style = MaterialTheme.typography.labelSmall,
                                    fontWeight = FontWeight.Bold
                                )
                            }"""

replacement_ghost_text = """                            Box(
                                modifier = Modifier
                                    .offset(x = ghostXOffset, y = ghostYOffset - 24.dp)
                                    .background(borderColor, RectangleShape)
                                    .padding(horizontal = 6.dp, vertical = 2.dp)
                            ) {
                                Text(
                                    text = "[ $startStr - $endStr ]",
                                    fontFamily = FontFamily.Monospace,
                                    color = MaterialTheme.colorScheme.onPrimary,
                                    style = MaterialTheme.typography.labelSmall,
                                    fontWeight = FontWeight.Bold
                                )
                            }"""

content = content.replace(target_ghost_text, replacement_ghost_text)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
print("Ghost Block Patched")
