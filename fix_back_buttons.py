import re

files = [
    "app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt",
    "app/src/main/java/com/example/ui/screens/UserAccountScreen.kt",
    "app/src/main/java/com/example/ui/screens/SettingsScreen.kt",
    "app/src/main/java/com/example/ui/screens/DeveloperOptionsScreen.kt",
    "app/src/main/java/com/example/ui/screens/UpdateLogScreen.kt",
]

for file_path in files:
    with open(file_path, "r") as f:
        content = f.read()

    # Add Menu import if not present
    if "import androidx.compose.material.icons.filled.Menu" not in content and "import androidx.compose.material.icons.filled.*" not in content:
        content = content.replace("import androidx.compose.material.icons.Icons", "import androidx.compose.material.icons.Icons\nimport androidx.compose.material.icons.filled.Menu")
    
    # Replace the icon
    content = re.sub(r'Icon\(Icons\.AutoMirrored\.Filled\.ArrowBack, contentDescription = "Back"\)', r'Icon(Icons.Default.Menu, contentDescription = "Menu")', content)
    content = re.sub(r'Icon\(Icons\.Default\.ArrowBack, contentDescription = "Back"\)', r'Icon(Icons.Default.Menu, contentDescription = "Menu")', content)

    with open(file_path, "w") as f:
        f.write(content)

