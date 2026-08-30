with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

import re

# Clean up the messed up lines
content = re.sub(r'• What was the friction point that broke my discipline\?• How did I handle stress or adversity today\?", isDefault = true\),\n', '', content)
content = re.sub(r'• Am I acting out of habit, or out of intention\?• What did I learn about myself in today\'s quiet moments\?", isDefault = true\),\n', '', content)

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
