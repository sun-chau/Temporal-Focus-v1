import os

path = 'app/src/main/java/com/example/ui/screens/UserAccountScreen.kt'
with open(path, 'r') as f:
    content = f.read()

target = """                TextButton(onClick = { launcher.launch("image/*") }) {
                    Text("Change Photo")
                }"""

replacement = """                Row(
                    horizontalArrangement = Arrangement.Center,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    TextButton(onClick = { launcher.launch("image/*") }) {
                        Text(if (imageUri.isNotEmpty()) "Change Photo" else "Add Photo")
                    }
                    if (imageUri.isNotEmpty()) {
                        TextButton(onClick = { 
                            imageUri = ""
                            viewModel.updateProfile(name, bio, imageUri)
                        }) {
                            Text("Remove Photo", color = MaterialTheme.colorScheme.error)
                        }
                    }
                }"""

if target in content:
    content = content.replace(target, replacement)
    with open(path, 'w') as f:
        f.write(content)
    print("Replaced successfully")
else:
    print("Target not found")
