import re

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

# Add imports
if "import androidx.compose.ui.text.input.VisualTransformation" not in content:
    content = content.replace("import androidx.compose.ui.text.input.PasswordVisualTransformation", "import androidx.compose.ui.text.input.PasswordVisualTransformation\nimport androidx.compose.ui.text.input.VisualTransformation\nimport androidx.compose.material.icons.filled.Visibility\nimport androidx.compose.material.icons.filled.VisibilityOff")
elif "import androidx.compose.material.icons.filled.Visibility" not in content:
    content = content.replace("import androidx.compose.material.icons.filled.KeyboardArrowRight", "import androidx.compose.material.icons.filled.KeyboardArrowRight\nimport androidx.compose.ui.text.input.PasswordVisualTransformation\nimport androidx.compose.ui.text.input.VisualTransformation\nimport androidx.compose.material.icons.filled.Visibility\nimport androidx.compose.material.icons.filled.VisibilityOff")

search = '''            var passwordInput by remember { mutableStateOf(uiState.appPassword) }'''
replace = '''            var passwordInput by remember { mutableStateOf(uiState.appPassword) }
            var passwordVisible by remember { mutableStateOf(false) }'''
content = content.replace(search, replace)

search_tf = '''                    OutlinedTextField(
                        value = passwordInput,
                        onValueChange = { 
                            passwordInput = it
                            viewModel.setAppPassword(it)
                        },
                        label = { Text("Password") },
                        singleLine = true,
                        modifier = Modifier.fillMaxWidth()
                    )'''
replace_tf = '''                    OutlinedTextField(
                        value = passwordInput,
                        onValueChange = { 
                            passwordInput = it
                            viewModel.setAppPassword(it)
                        },
                        label = { Text("Password") },
                        visualTransformation = if (passwordVisible) VisualTransformation.None else PasswordVisualTransformation(),
                        trailingIcon = {
                            val image = if (passwordVisible) Icons.Filled.Visibility else Icons.Filled.VisibilityOff
                            val description = if (passwordVisible) "Hide password" else "Show password"
                            IconButton(onClick = { passwordVisible = !passwordVisible }) {
                                Icon(imageVector = image, contentDescription = description)
                            }
                        },
                        singleLine = true,
                        modifier = Modifier.fillMaxWidth()
                    )'''
content = content.replace(search_tf, replace_tf)

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)
