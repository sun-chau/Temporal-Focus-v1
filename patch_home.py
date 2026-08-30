import re

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    content = f.read()

# I will replace the Icon line with an explicit import and use of Add
if 'import androidx.compose.material.icons.filled.Add' not in content:
    content = content.replace('import androidx.compose.material.icons.filled.Menu', 'import androidx.compose.material.icons.filled.Menu\nimport androidx.compose.material.icons.filled.Add')

content = content.replace('androidx.compose.material.icons.Icons.Default.Add', 'androidx.compose.material.icons.Icons.Default.Add')

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(content)

