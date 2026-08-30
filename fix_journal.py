import re

with open('app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt', 'r') as f:
    content = f.read()

bad_str = 'content += "\n- "'
good_str = 'content += "\\n- "'

content = content.replace(bad_str, good_str)

with open('app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt', 'w') as f:
    f.write(content)
