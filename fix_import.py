with open("app/src/main/java/com/example/ui/screens/CustomTrackerUI.kt", "r") as f:
    content = f.read()

content = content.replace("import androidx.compose.foundation.horizontalScroll", "import androidx.compose.foundation.horizontalScroll\nimport androidx.compose.foundation.verticalScroll")

with open("app/src/main/java/com/example/ui/screens/CustomTrackerUI.kt", "w") as f:
    f.write(content)
