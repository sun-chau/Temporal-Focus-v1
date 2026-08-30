import re

with open("app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt", "r") as f:
    content = f.read()

# The file might end with `    }\n}\n}\n}` or similar.
# Let's clean up the trailing braces.
# We know CompletedTimerCard needs 3 braces at the end.
# Surface { Text } -> }
# Column -> }
# Card -> }
# CompletedTimerCard -> }
# So it should be 4 braces. Let's see what is actually there.

search_str = r'            \}\n        \}\n    \}\n\}\n?\}?\n?'
replace_str = '            }\n        }\n    }\n}\n'

content = re.sub(search_str, replace_str, content)

with open("app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt", "w") as f:
    f.write(content)
