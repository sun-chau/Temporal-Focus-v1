with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

start_idx = content.find("                        androidx.compose.foundation.layout.Box(")
if start_idx == -1:
    print("Could not find start_idx")
    exit(1)
start_idx = content.find("}", start_idx + 500)  # Find the } that closes the inner loop
if start_idx == -1:
    print("Could not find start_idx 2")
    exit(1)

end_idx = content.find("    if (showDatePicker) {")
if end_idx == -1:
    print("Could not find end_idx")
    exit(1)

# Let's extract the part before start_idx + a little bit to see where we are
# Actually, I know exactly what needs to be from the end of the dashed border lines:
# 
#                                     )
#                                 }
#                         )
#                     }
#                 }
#                 
#                 // Current Time Indicator
#                 if (page == actualTodayPage) {
#                     ...
#                 }
#             }
#         }
#     }
#     
#     if (showDatePicker) {

# Let's just use regex to replace everything between "        pathEffect = androidx.compose.ui.graphics.PathEffect.dashPathEffect(floatArrayOf(10f, 10f), 0f)" and "    if (showDatePicker) {"

import re
pattern = r"pathEffect = androidx.compose.ui.graphics.PathEffect.dashPathEffect\(floatArrayOf\(10f, 10f\), 0f\)\s*\)\s*}\s*\)\s*}\s*}\s*(?:// Current Time Indicator\s*if \(page == actualTodayPage\) \{.*?)?(?:val cal.*?)?.*?\s*}\s*}\s*}\s*if \(showDatePicker\) \{"

# Since re.sub can be tricky with so many newlines, let's do a find and string slicing.
marker1 = "pathEffect = androidx.compose.ui.graphics.PathEffect.dashPathEffect(floatArrayOf(10f, 10f), 0f)"
idx1 = content.find(marker1)
idx1 = content.find(")", idx1)
idx1 = content.find("}", idx1)
idx1 = content.find(")", idx1)
# we are at the end of the Box for the dashed line
end_dashed_box = idx1 + 1

idx_show_date = content.find("    if (showDatePicker) {", end_dashed_box)

new_block = """
                        )
                    }
                }
                
                // Current Time Indicator
                if (page == actualTodayPage) {
                    val cal = java.util.Calendar.getInstance()
                    val currentMinutes = cal.get(java.util.Calendar.HOUR_OF_DAY) * 60 + cal.get(java.util.Calendar.MINUTE)
                    val xOffset = (currentMinutes * 2.0f).dp
                    
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
    }
    
    if (showDatePicker) {"""

clean_content = content[:content.rfind(")", 0, end_dashed_box)] + new_block + content[idx_show_date + len("    if (showDatePicker) {"):]
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(clean_content)
print("Applied clean block!")
