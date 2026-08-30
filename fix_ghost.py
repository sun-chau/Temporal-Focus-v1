import re
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

ghost_block = """
                        if (isCreatingGhost) {
                            val startCal = Calendar.getInstance().apply { timeInMillis = ghostStartTimeMillis }
                            val startMinutes = if (ghostStartTimeMillis < startOfDay) 0 else startCal.get(Calendar.HOUR_OF_DAY) * 60 + startCal.get(Calendar.MINUTE)
                            val endMinutes = if (ghostEndTimeMillis > endOfDay) 24 * 60 else {
                                val endCal = Calendar.getInstance().apply { timeInMillis = ghostEndTimeMillis }
                                endCal.get(Calendar.HOUR_OF_DAY) * 60 + endCal.get(Calendar.MINUTE)
                            }
                            val durationMinutes = maxOf(10, endMinutes - startMinutes)
                            val ghostXOffset = (startMinutes * 1.5f).dp
                            val ghostYOffset = (ghostLaneIndex * 80 + 4).dp
                            val ghostWidth = (durationMinutes * 1.5f).dp
                            
                            val isWarning = isGhostColliding
                            val borderColor = if (isWarning) Color.Red else MaterialTheme.colorScheme.primary
                            val bgColor = if (isWarning) Color.Red.copy(alpha = 0.3f) else MaterialTheme.colorScheme.primary.copy(alpha = 0.1f)
                            
                            Box(
                                modifier = Modifier
                                    .offset(x = ghostXOffset, y = ghostYOffset)
                                    .width(ghostWidth)
                                    .height(72.dp)
                                    .clip(RoundedCornerShape(8.dp))
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
                                    }
                            ) {
                                val startStr = String.format("%02d:%02d", startCal.get(Calendar.HOUR_OF_DAY), startCal.get(Calendar.MINUTE))
                                val endCal = Calendar.getInstance().apply { timeInMillis = ghostEndTimeMillis }
                                val endStr = String.format("%02d:%02d", endCal.get(Calendar.HOUR_OF_DAY), endCal.get(Calendar.MINUTE))
                                Text(
                                    text = "$startStr - $endStr",
                                    color = if (isWarning) Color.Red else MaterialTheme.colorScheme.primary,
                                    style = MaterialTheme.typography.labelSmall,
                                    modifier = Modifier.align(Alignment.Center)
                                )
                            }
                        }

                        if (isToday) {"""

content = content.replace("                        if (isToday) {", ghost_block)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
