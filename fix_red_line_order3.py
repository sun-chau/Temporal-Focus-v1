import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

target = """    }
    }
    }
       
    if (showDatePicker) {"""

replacement = """    }
    
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
    }
    }
       
    if (showDatePicker) {"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
print("Inserted successfully")
