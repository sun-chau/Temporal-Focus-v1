import re
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Replace the boundary boxes
pattern = r"androidx\.compose\.foundation\.layout\.Box\(\n\s*modifier = Modifier\n\s*\.fillMaxHeight\(\)\n\s*\.width\(1\.dp\)\n\s*\.align\(Alignment\.CenterStart\)\n\s*\.background\(MaterialTheme\.colorScheme\.outlineVariant\)\n\s*\)"
repl = """androidx.compose.foundation.layout.Box(
                            modifier = Modifier
                                .fillMaxHeight()
                                .width(1.dp)
                                .align(Alignment.CenterStart)
                                .drawBehind {
                                    drawLine(
                                        color = outlineColor,
                                        start = androidx.compose.ui.geometry.Offset(0f, 0f),
                                        end = androidx.compose.ui.geometry.Offset(0f, size.height),
                                        strokeWidth = 1.dp.toPx(),
                                        pathEffect = androidx.compose.ui.graphics.PathEffect.dashPathEffect(floatArrayOf(10f, 10f), 0f)
                                    )
                                }
                        )"""
                        
pattern2 = r"androidx\.compose\.foundation\.layout\.Box\(\n\s*modifier = Modifier\n\s*\.fillMaxHeight\(\)\n\s*\.width\(1\.dp\)\n\s*\.align\(Alignment\.CenterEnd\)\n\s*\.background\(MaterialTheme\.colorScheme\.outlineVariant\)\n\s*\)"
repl2 = """androidx.compose.foundation.layout.Box(
                            modifier = Modifier
                                .fillMaxHeight()
                                .width(1.dp)
                                .align(Alignment.CenterEnd)
                                .drawBehind {
                                    drawLine(
                                        color = outlineColor,
                                        start = androidx.compose.ui.geometry.Offset(0f, 0f),
                                        end = androidx.compose.ui.geometry.Offset(0f, size.height),
                                        strokeWidth = 1.dp.toPx(),
                                        pathEffect = androidx.compose.ui.graphics.PathEffect.dashPathEffect(floatArrayOf(10f, 10f), 0f)
                                    )
                                }
                        )"""

# add outlineColor above boundary lines
content = content.replace("// Boundary lines", "val outlineColor = MaterialTheme.colorScheme.outlineVariant\n                        // Boundary lines")

content = re.sub(pattern, repl, content)
content = re.sub(pattern2, repl2, content)
content = content.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\nimport androidx.compose.ui.draw.drawBehind")

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
