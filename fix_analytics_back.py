import re
file_path = "app/src/main/java/com/example/ui/screens/AnalyticsDashboardScreen.kt"
with open(file_path, "r") as f:
    content = f.read()

if "import androidx.compose.material.icons.filled.Menu" not in content:
    content = content.replace("import androidx.compose.material.icons.Icons", "import androidx.compose.material.icons.Icons\nimport androidx.compose.material.icons.filled.Menu")

content = re.sub(r'Icon\(Icons\.AutoMirrored\.Filled\.ArrowBack, contentDescription = "Back"\)', r'Icon(Icons.Default.Menu, contentDescription = "Menu")', content)

with open(file_path, "w") as f:
    f.write(content)
