import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# 1. Remove red line from before Canvas Body
target_remove = """                // Current Time Indicator
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
                }"""
content = content.replace(target_remove, "")

# 2. Add red line at the end of Canvas Body
target_add = """                        )
                    }
                }
                   

    }"""
replacement_add = """                        )
                    }
                }
                
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
content = content.replace(target_add, replacement_add)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
print("Red line moved to top z-index")
