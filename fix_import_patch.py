with open("app/src/main/java/com/example/ui/screens/UserAccountScreen.kt", "r") as f:
    content = f.read()

content = content.replace("import androidx.compose.foundation.BorderStroke\npackage", "package")
content = content.replace("import android.net.Uri", "import androidx.compose.foundation.BorderStroke\nimport android.net.Uri")

with open("app/src/main/java/com/example/ui/screens/UserAccountScreen.kt", "w") as f:
    f.write(content)
