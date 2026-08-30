import re

with open("app/src/main/java/com/example/ui/screens/MainScreen.kt", "r") as f:
    content = f.read()

# Remove the description "Dual-engine temporal alignment & focus suite" and its spacer
content = re.sub(r'                            Spacer\(modifier = Modifier\.height\(4\.dp\)\)\n                            Text\(\n                                text = "Dual-engine temporal alignment & focus suite",\n                                style = MaterialTheme\.typography\.bodySmall,\n                                color = MaterialTheme\.colorScheme\.onSurfaceVariant,\n                                lineHeight = 14\.sp\n                            \)', '', content)

# Change help button to "coming soon"
help_old = r'''                    NavigationDrawerItem\(
                        icon = \{ Icon\(Icons\.Outlined\.HelpOutline, contentDescription = null\) \},
                        label = \{ Text\("Help & FAQ"\) \},
                        selected = false,
                        onClick = \{
                            scope\.launch \{ drawerState\.close\(\) \}
                            showHelpDialog = true
                        \},'''
help_new = '''                    NavigationDrawerItem(
                        icon = { Icon(Icons.Outlined.HelpOutline, contentDescription = null) },
                        label = { Text("Help & FAQ") },
                        selected = false,
                        onClick = {
                            scope.launch { drawerState.close() }
                            android.widget.Toast.makeText(context, "Coming soon", android.widget.Toast.LENGTH_SHORT).show()
                        },'''
content = re.sub(help_old, help_new, content)

with open("app/src/main/java/com/example/ui/screens/MainScreen.kt", "w") as f:
    f.write(content)
