import re

with open("app/src/main/java/com/example/ui/screens/CircularMenu.kt", "r") as f:
    content = f.read()

search_items = r'''                    val items = mutableListOf\(
                        Triple\(Icons\.Outlined\.Check, onComplete, if \(isOverdue\) MaterialTheme\.colorScheme\.primary else MaterialTheme\.colorScheme\.primary\.copy\(alpha = 0\.4f\)\),
                        Triple\(Icons\.Outlined\.Edit, onEdit, Color\.White\),
                        Triple\(Icons\.Outlined\.Info, onInfo, Color\.White\)
                    \)'''

replace_items = '''                    val items = mutableListOf(
                        Triple(Icons.Outlined.Check, onComplete, MaterialTheme.colorScheme.primary),
                        Triple(Icons.Outlined.Edit, onEdit, Color.White),
                        Triple(Icons.Outlined.Info, onInfo, Color.White)
                    )'''

content = re.sub(search_items, replace_items, content)

search_click = r'''                            onClick = \{ 
                                 if \(\(icon == Icons\.Outlined\.Check || icon == Icons\.Default\.FastForward\) && !isOverdue\) \{
                                    android\.widget\.Toast\.makeText\(context, "Still some time left, wait\.", android\.widget\.Toast\.LENGTH_SHORT\)\.show\(\)
                                    expanded = false
                                \} else \{
                                    action\(\)
                                    expanded = false 
                                \}
                             \},'''

replace_click = '''                            onClick = { 
                                 if (icon == Icons.Default.FastForward && !isOverdue) {
                                    android.widget.Toast.makeText(context, "Still some time left, wait.", android.widget.Toast.LENGTH_SHORT).show()
                                    expanded = false
                                } else {
                                    action()
                                    expanded = false 
                                }
                             },'''

content = re.sub(search_click, replace_click, content)

with open("app/src/main/java/com/example/ui/screens/CircularMenu.kt", "w") as f:
    f.write(content)
