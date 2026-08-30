with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# I currently have:
# }
# }
# }
# 
# @Composable
# fun DateNavigator
#
# I need to change it to:
# }
# }
# 
# @Composable
# fun DateNavigator

content = content.replace("}\n}\n}\n\n@Composable\nfun DateNavigator", "}\n}\n\n@Composable\nfun DateNavigator")

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
