import re
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

pattern = r"Box\(\n\s*modifier = Modifier\n\s*\.width\(blockWidth\)\n\s*\.fillMaxHeight\(\)\n\s*\.clip\(RoundedCornerShape\(8\.dp\)\)\n\s*\.background\(blockBackgroundColor\)\n\s*\.border\(blockBorderWidth, blockBorderColor, RoundedCornerShape\(8\.dp\)\)\n\s*\.clickable \{ onClick\(\) \}\n\s*\)"

repl = """val shape = RoundedCornerShape(
            topStart = if (isBleedLeft) 0.dp else 8.dp,
            bottomStart = if (isBleedLeft) 0.dp else 8.dp,
            topEnd = if (isBleedRight) 0.dp else 8.dp,
            bottomEnd = if (isBleedRight) 0.dp else 8.dp
        )
        
        Box(
            modifier = Modifier
                .width(blockWidth)
                .fillMaxHeight()
                .clip(shape)
                .background(blockBackgroundColor)
                .drawBehind {
                    val stroke = androidx.compose.ui.graphics.drawscope.Stroke(blockBorderWidth.toPx())
                    val halfStroke = blockBorderWidth.toPx() / 2f
                    val cornerRadius = 8.dp.toPx()
                    
                    val path = androidx.compose.ui.graphics.Path().apply {
                        if (isBleedLeft) {
                            moveTo(0f, halfStroke)
                        } else {
                            moveTo(cornerRadius, halfStroke)
                        }
                        
                        // Top edge
                        if (isBleedRight) {
                            lineTo(size.width, halfStroke)
                        } else {
                            lineTo(size.width - cornerRadius, halfStroke)
                            arcTo(
                                rect = androidx.compose.ui.geometry.Rect(size.width - 2 * cornerRadius, halfStroke, size.width - halfStroke, 2 * cornerRadius - halfStroke),
                                startAngleDegrees = -90f,
                                sweepAngleDegrees = 90f,
                                forceMoveTo = false
                            )
                        }
                        
                        // Right edge
                        if (!isBleedRight) {
                            lineTo(size.width - halfStroke, size.height - cornerRadius)
                            arcTo(
                                rect = androidx.compose.ui.geometry.Rect(size.width - 2 * cornerRadius, size.height - 2 * cornerRadius + halfStroke, size.width - halfStroke, size.height - halfStroke),
                                startAngleDegrees = 0f,
                                sweepAngleDegrees = 90f,
                                forceMoveTo = false
                            )
                        } else {
                            moveTo(size.width, size.height - halfStroke)
                        }
                        
                        // Bottom edge
                        if (isBleedLeft) {
                            lineTo(0f, size.height - halfStroke)
                        } else {
                            lineTo(cornerRadius, size.height - halfStroke)
                            arcTo(
                                rect = androidx.compose.ui.geometry.Rect(halfStroke, size.height - 2 * cornerRadius + halfStroke, 2 * cornerRadius - halfStroke, size.height - halfStroke),
                                startAngleDegrees = 90f,
                                sweepAngleDegrees = 90f,
                                forceMoveTo = false
                            )
                        }
                        
                        // Left edge
                        if (!isBleedLeft) {
                            lineTo(halfStroke, cornerRadius)
                            arcTo(
                                rect = androidx.compose.ui.geometry.Rect(halfStroke, halfStroke, 2 * cornerRadius - halfStroke, 2 * cornerRadius - halfStroke),
                                startAngleDegrees = 180f,
                                sweepAngleDegrees = 90f,
                                forceMoveTo = false
                            )
                        } else {
                            moveTo(0f, halfStroke)
                        }
                    }
                    drawPath(path, blockBorderColor, style = stroke)
                }
                .clickable { onClick() }
        )"""

content = re.sub(pattern, repl, content)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
