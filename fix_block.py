with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    lines = f.readlines()

new_lines = []
in_bad_zone = False
for i, line in enumerate(lines):
    if i == 456: # line 457
        new_lines.append("""                            ) {
                                val startStr = String.format("%02d:%02d", startCal.get(java.util.Calendar.HOUR_OF_DAY), startCal.get(java.util.Calendar.MINUTE))
                                val endCal = java.util.Calendar.getInstance().apply { timeInMillis = ghostEndTimeMillis }
                                val endStr = String.format("%02d:%02d", endCal.get(java.util.Calendar.HOUR_OF_DAY), endCal.get(java.util.Calendar.MINUTE))
                                androidx.compose.material3.Text(
                                    text = "$startStr - $endStr",
                                    color = if (isWarning) androidx.compose.ui.graphics.Color.Red else androidx.compose.material3.MaterialTheme.colorScheme.primary,
                                    style = androidx.compose.material3.MaterialTheme.typography.labelSmall,
                                    modifier = androidx.compose.ui.Modifier.align(androidx.compose.ui.Alignment.Center)
                                )
                            }
                        }
                    }
                }
                
                val outlineColor = androidx.compose.material3.MaterialTheme.colorScheme.onSurface.copy(alpha = 0.8f)
                // Boundary lines
                androidx.compose.foundation.layout.Box(
                    modifier = androidx.compose.ui.Modifier
                        .fillMaxHeight()
                        .width(2.dp)
                        .align(androidx.compose.ui.Alignment.CenterStart)
                        .drawBehind {
                            drawLine(
                                color = outlineColor,
                                start = androidx.compose.ui.geometry.Offset(0f, 0f),
                                end = androidx.compose.ui.geometry.Offset(0f, size.height),
                                strokeWidth = 2.dp.toPx(),
                                pathEffect = androidx.compose.ui.graphics.PathEffect.dashPathEffect(floatArrayOf(10f, 10f), 0f)
                            )
                        }
                )
                
                androidx.compose.foundation.layout.Box(
                    modifier = androidx.compose.ui.Modifier
                        .fillMaxHeight()
                        .width(2.dp)
                        .align(androidx.compose.ui.Alignment.CenterEnd)
                        .drawBehind {
                            drawLine(
                                color = outlineColor,
                                start = androidx.compose.ui.geometry.Offset(0f, 0f),
                                end = androidx.compose.ui.geometry.Offset(0f, size.height),
                                strokeWidth = 2.dp.toPx(),
                                pathEffect = androidx.compose.ui.graphics.PathEffect.dashPathEffect(floatArrayOf(10f, 10f), 0f)
                            )
                        }
                )
                
                // Current Time Indicator
                if (page == actualTodayPage) {
                    val cal = java.util.Calendar.getInstance()
                    val currentMinutes = cal.get(java.util.Calendar.HOUR_OF_DAY) * 60 + cal.get(java.util.Calendar.MINUTE)
                    val xOffset = (currentMinutes * 2.0f).dp
                    
                    androidx.compose.foundation.layout.Box(
                        modifier = androidx.compose.ui.Modifier
                            .offset(x = xOffset)
                            .width(2.dp)
                            .fillMaxHeight()
                            .background(androidx.compose.ui.graphics.Color.Red)
                            .onGloballyPositioned { coordinates ->
                                val windowBounds = coordinates.boundsInWindow()
                                isNowLineVisible = windowBounds.right > 0 && windowBounds.left < screenWidthPx
                            }
                    )
                }
            }
        }
    }
""")
        in_bad_zone = True
    elif in_bad_zone:
        if "    if (showDatePicker) {" in line:
            in_bad_zone = False
            new_lines.append(line)
    else:
        new_lines.append(line)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.writelines(new_lines)

print("Applied strict line-based fix!")
