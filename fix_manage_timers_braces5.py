import re

with open("app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt", "r") as f:
    content = f.read()

# Replace the block right before ActiveQueueTab
# It currently has something like `        }}@Composable\nfun ActiveQueueTab`
content = re.sub(r'\}\s*\}\s*@Composable\nfun ActiveQueueTab', '}\n    }\n}\n\n@Composable\nfun ActiveQueueTab', content)

with open("app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt", "w") as f:
    f.write(content)
