import re

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "r") as f:
    content = f.read()

content = re.sub(
r'''IconButton\(
                            onClick = \{ viewModel\.setCreatingChronometer\(true\) \},
                            modifier = Modifier
                                \.fillMaxSize\(\)
                                \.clip\(CircleShape\)
                                \.background\(MaterialTheme\.colorScheme\.primary\)
                        \) \{
                            Icon\(Icons\.Default\.Add, contentDescription = "Create", tint = MaterialTheme\.colorScheme\.background, modifier = Modifier\.size\(40\.dp\)\)
                        \}''',
r'''Box(
                            modifier = Modifier
                                .fillMaxSize()
                                .clip(CircleShape)
                                .background(MaterialTheme.colorScheme.primary)
                                .clickable { viewModel.setCreatingChronometer(true) },
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.Add, contentDescription = "Create", tint = MaterialTheme.colorScheme.background, modifier = Modifier.size(40.dp))
                        }''', content)

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "w") as f:
    f.write(content)
