import re

with open("app/src/main/java/com/example/ui/screens/SecuritySettingsScreen.kt", "r") as f:
    content = f.read()

old_switch = """Switch(
                        checked = uiState.biometricAuthEnabled,
                        onCheckedChange = { 
                            if (!uiState.biometricAuthEnabled) {
                                viewModel.setBiometricAuthEnabled(true)
                            } else {
                                viewModel.setBiometricAuthEnabled(false)
                            }
                        }
                    )"""

new_switch = """Switch(
                        checked = uiState.biometricAuthEnabled,
                        onCheckedChange = { 
                            if (!uiState.biometricAuthEnabled) {
                                viewModel.setBiometricAuthEnabled(true)
                            } else {
                                viewModel.setBiometricAuthEnabled(false)
                            }
                        },
                        colors = androidx.compose.material3.SwitchDefaults.colors(
                            checkedThumbColor = androidx.compose.material3.MaterialTheme.colorScheme.surface,
                            checkedTrackColor = androidx.compose.material3.MaterialTheme.colorScheme.primary,
                            checkedIconColor = androidx.compose.material3.MaterialTheme.colorScheme.primary,
                            uncheckedThumbColor = androidx.compose.material3.MaterialTheme.colorScheme.onSurface,
                            uncheckedTrackColor = androidx.compose.material3.MaterialTheme.colorScheme.surfaceVariant,
                            uncheckedIconColor = androidx.compose.material3.MaterialTheme.colorScheme.surface
                        ),
                        thumbContent = if (uiState.biometricAuthEnabled) {
                            {
                                androidx.compose.material3.Icon(
                                    imageVector = androidx.compose.material.icons.Icons.Filled.Check,
                                    contentDescription = null,
                                    modifier = Modifier.size(androidx.compose.material3.SwitchDefaults.IconSize),
                                )
                            }
                        } else {
                            {
                                androidx.compose.material3.Icon(
                                    imageVector = androidx.compose.material.icons.Icons.Filled.Close,
                                    contentDescription = null,
                                    modifier = Modifier.size(androidx.compose.material3.SwitchDefaults.IconSize),
                                )
                            }
                        }
                    )"""

content = content.replace(old_switch, new_switch)

if "import androidx.compose.material.icons.filled.Check" not in content:
    content = content.replace("import androidx.compose.material.icons.Icons", "import androidx.compose.material.icons.Icons\nimport androidx.compose.material.icons.filled.Check\nimport androidx.compose.material.icons.filled.Close\n")

with open("app/src/main/java/com/example/ui/screens/SecuritySettingsScreen.kt", "w") as f:
    f.write(content)
