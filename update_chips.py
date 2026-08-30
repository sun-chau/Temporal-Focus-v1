import re

with open("app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt", "r") as f:
    content = f.read()

# Replace button color for chips
button_replacement = r'Button(onClick = { \1 }, modifier = chipModifier, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f), contentColor = MaterialTheme.colorScheme.onSurface), contentPadding = PaddingValues(0.dp)) { Text("\2", fontSize = 12.sp) }'

content = re.sub(r'Button\(onClick = \{ ([^}]+) \}, modifier = chipModifier, contentPadding = PaddingValues\(0\.dp\)\) \{ Text\("([^"]+)", fontSize = 12\.sp\) \}', button_replacement, content)

with open("app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt", "w") as f:
    f.write(content)
