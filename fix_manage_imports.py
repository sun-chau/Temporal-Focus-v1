import re

with open("app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt", "r") as f:
    content = f.read()

if "import androidx.compose.material3.SwipeToDismissBox" not in content:
    content = content.replace("import androidx.compose.material3.*", "import androidx.compose.material3.*\nimport androidx.compose.material3.SwipeToDismissBox\nimport androidx.compose.material3.SwipeToDismissBoxValue\nimport androidx.compose.material3.rememberSwipeToDismissBoxState")

if "import androidx.compose.animation.animateColorAsState" not in content:
    content = content.replace("import androidx.compose.runtime.*", "import androidx.compose.runtime.*\nimport androidx.compose.animation.animateColorAsState")

with open("app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt", "w") as f:
    f.write(content)
