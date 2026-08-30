import re

with open("app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt", "r") as f:
    content = f.read()

trailing_icon_old = r'''                    trailingIcon = \{
                        IconButton\(onClick = \{ keyboardController\?\.hide\(\) \}\) \{
                            Icon\(Icons\.Default\.Check, contentDescription = "Done"\)
                        \}
                    \},'''

trailing_icon_new = '''                    trailingIcon = {
                        Row {
                            val context = androidx.compose.ui.platform.LocalContext.current
                            IconButton(onClick = { android.widget.Toast.makeText(context, "Coming soon", android.widget.Toast.LENGTH_SHORT).show() }) {
                                Icon(androidx.compose.material.icons.Icons.Default.AttachFile, contentDescription = "Attachment")
                            }
                            IconButton(onClick = { keyboardController?.hide() }) {
                                Icon(Icons.Default.Check, contentDescription = "Done")
                            }
                        }
                    },'''

content = re.sub(trailing_icon_old, trailing_icon_new, content)

if "import androidx.compose.material.icons.filled.AttachFile" not in content:
    content = content.replace("import androidx.compose.material.icons.filled.Check", "import androidx.compose.material.icons.filled.Check\nimport androidx.compose.material.icons.filled.AttachFile")

with open("app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt", "w") as f:
    f.write(content)
