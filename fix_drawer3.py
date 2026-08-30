import re

with open("app/src/main/java/com/example/ui/screens/MainScreen.kt", "r") as f:
    content = f.read()

# Let's fix the header.
# We'll just replace the entire header.
search_str = r'''                Column\(
                    modifier = Modifier
                        \.fillMaxWidth\(\)
                        \.background\(MaterialTheme\.colorScheme\.primary\.copy\(alpha = 0\.08f\)\)
                        \.padding\(24\.dp\)
                \) \{[\s\S]+?HorizontalDivider'''

new_header = '''                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.08f))
                        .padding(24.dp)
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .size(48.dp)
                                .clip(RoundedCornerShape(12.dp))
                                .background(MaterialTheme.colorScheme.primary),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Default.HourglassEmpty,
                                contentDescription = "App Icon",
                                tint = MaterialTheme.colorScheme.onPrimary,
                                modifier = Modifier.size(28.dp)
                            )
                        }
                        Spacer(modifier = Modifier.width(16.dp))
                        Column {
                            Text(
                                text = "Temporal Focus",
                                style = MaterialTheme.typography.titleLarge,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.onSurface
                            )
                            Spacer(modifier = Modifier.height(4.dp))
                            Box(
                                modifier = Modifier
                                    .border(1.dp, MaterialTheme.colorScheme.primary.copy(alpha = 0.5f), RoundedCornerShape(50))
                                    .padding(horizontal = 6.dp, vertical = 2.dp)
                            ) {
                                Text(
                                    text = "v${updateLogs.firstOrNull()?.timestamp ?: com.example.BuildConfig.VERSION_NAME}",
                                    style = MaterialTheme.typography.labelSmall,
                                    color = MaterialTheme.colorScheme.primary,
                                    fontWeight = FontWeight.Bold
                                )
                            }
                        }
                    }
                }
                
                HorizontalDivider'''

content = re.sub(search_str, new_header, content)

# And let's fix the help button
help_old = r'''                    NavigationDrawerItem\(
                        icon = \{ Icon\(Icons\.Outlined\.HelpOutline, contentDescription = null\) \},
                        label = \{ Text\("Help"\) \},
                        selected = false,
                        onClick = \{
                            scope\.launch \{ drawerState\.close\(\) \}
                            showHelpDialog = true
                        \},'''

help_new = '''                    NavigationDrawerItem(
                        icon = { Icon(Icons.Outlined.HelpOutline, contentDescription = null) },
                        label = { Text("Help") },
                        selected = false,
                        onClick = {
                            scope.launch { drawerState.close() }
                            android.widget.Toast.makeText(context, "Coming soon", android.widget.Toast.LENGTH_SHORT).show()
                        },'''

content = re.sub(help_old, help_new, content)

with open("app/src/main/java/com/example/ui/screens/MainScreen.kt", "w") as f:
    f.write(content)
