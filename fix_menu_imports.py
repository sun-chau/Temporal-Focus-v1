def add_menu_import(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    if "import androidx.compose.material.icons.filled.Menu" not in content:
        content = content.replace("import androidx.compose.material.icons.filled.Info", "import androidx.compose.material.icons.filled.Info\nimport androidx.compose.material.icons.filled.Menu")
        with open(file_path, "w") as f:
            f.write(content)

add_menu_import("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt")
add_menu_import("app/src/main/java/com/example/ui/screens/PomodoroScreen.kt")
