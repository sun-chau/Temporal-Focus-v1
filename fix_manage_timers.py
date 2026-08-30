import re

with open("app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt", "r") as f:
    content = f.read()

content = content.replace(
    'IconButton(onClick = { android.widget.Toast.makeText(context, "Coming soon", android.widget.Toast.LENGTH_SHORT).show() }, enabled = false) {',
    'IconButton(onClick = { android.widget.Toast.makeText(context, "Coming soon", android.widget.Toast.LENGTH_SHORT).show() }) {'
)
content = content.replace(
    'Icon(Icons.Outlined.Brightness4, contentDescription = "Daily Schedule (Routine)")',
    'Icon(Icons.Outlined.Brightness4, contentDescription = "Daily Schedule (Routine)", tint = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.4f))'
)

with open("app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt", "w") as f:
    f.write(content)
