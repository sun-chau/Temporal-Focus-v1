import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# I messed up the red line insertion and swallowed 3 closing brackets.
# The original text was:
#                     }
#                 }
# 
#     }
#     }
#     }
#        
#     if (showDatePicker) {

# Let me first remove the Current Time Indicator that I just inserted.
start_idx = content.find("        // Current Time Indicator")
end_idx = content.find("    if (showDatePicker) {", start_idx)

if start_idx != -1 and end_idx != -1:
    clean_content = content[:start_idx] + """    }
    }
    }
       
""" + content[end_idx:]
    with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
        f.write(clean_content)
    print("Reverted bracket removal")
else:
    print("Could not find block")
