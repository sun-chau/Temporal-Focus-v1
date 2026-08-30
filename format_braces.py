import sys

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Let's fix the section from onDispose to DateNavigator
import re

# find onDispose { datePickerDialog.dismiss() }
start_idx = content.find("datePickerDialog.dismiss()")
if start_idx == -1:
    sys.exit("not found dismiss")

end_idx = content.find("@Composable\nfun DateNavigator", start_idx)
if end_idx == -1:
    sys.exit("not found DateNavigator")

# Replace everything in between with the correct braces
# We need:
#             }
#         }
#     }
# }
# }
# }
# 
# @Composable

replacement = """
            }
        }
    }
}
}
}

@Composable
fun DateNavigator"""

content = content[:start_idx + len("datePickerDialog.dismiss()")] + replacement + content[end_idx + len("@Composable\nfun DateNavigator"):]

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)

