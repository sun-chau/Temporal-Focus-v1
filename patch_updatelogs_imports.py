with open('/app/applet/app/src/main/java/com/example/ui/screens/UpdateLogScreen.kt', 'r') as f:
    content = f.read()

imports = """
import androidx.compose.ui.Alignment
import androidx.compose.material.icons.filled.ExpandLess
import androidx.compose.material.icons.filled.ExpandMore
"""

content = content.replace("import androidx.compose.ui.Modifier", imports + "import androidx.compose.ui.Modifier")

with open('/app/applet/app/src/main/java/com/example/ui/screens/UpdateLogScreen.kt', 'w') as f:
    f.write(content)

