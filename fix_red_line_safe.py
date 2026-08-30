import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Remove the previously botched inserted Red line from the end of the file.
start_idx = content.find("        // Current Time Indicator")
if start_idx != -1:
    end_idx = content.find("    if (showDatePicker) {", start_idx)
    if end_idx != -1:
        clean_content = content[:start_idx] + """    }
    }
       
""" + content[end_idx:]
        content = clean_content

# Now insert it at the end of the inner Box
target = """                                    )
                                }
                        )
                    }"""

replacement = """                                    )
                                }
                        )
                        
                        // Current Time Indicator
                        if (page == actualTodayPage) {
                            val cal = java.util.Calendar.getInstance()
                            val currentMinutes = cal.get(java.util.Calendar.HOUR_OF_DAY) * 60 + cal.get(java.util.Calendar.MINUTE)
                            val xOffset = (currentMinutes * 1.5f).dp
                            
                            androidx.compose.foundation.layout.Box(
                                modifier = Modifier
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
                    }"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
print("Red line placed safely")
