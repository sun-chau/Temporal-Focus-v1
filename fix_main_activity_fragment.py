path = 'app/src/main/java/com/example/MainActivity.kt'
with open(path, 'r') as f:
    content = f.read()

content = content.replace("import androidx.activity.ComponentActivity", "import androidx.activity.ComponentActivity\nimport androidx.fragment.app.FragmentActivity")
content = content.replace("class MainActivity : ComponentActivity()", "class MainActivity : FragmentActivity()")

with open(path, 'w') as f:
    f.write(content)
