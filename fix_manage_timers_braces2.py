import re

with open("app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt", "r") as f:
    content = f.read()

search_str = '''                }
            }
        }
}
@Composable'''

replace_str = '''                }
            }
        }
    }
}
@Composable'''

content = content.replace(search_str, replace_str)

with open("app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt", "w") as f:
    f.write(content)
