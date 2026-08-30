import re

with open("app/src/main/java/com/example/ui/screens/LoginScreen.kt", "r") as f:
    content = f.read()

content = content.replace("import androidx.compose.material.icons.filled.Login", "import androidx.compose.material.icons.automirrored.filled.Login")
content = content.replace("Icons.Default.Login", "Icons.AutoMirrored.Filled.Login")

content = content.replace("""            Button(
                onClick = { authenticateWithBiometrics() },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp),
                shape = unifiedShape,
                colors = ButtonDefaults.buttonColors(
                    containerColor = MaterialTheme.colorScheme.secondaryContainer, 
                    contentColor = MaterialTheme.colorScheme.onSecondaryContainer
                )
            ) {
                Icon(Icons.Default.Fingerprint, contentDescription = "Biometrics", modifier = Modifier.size(20.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text("Unlock with Biometrics", style = MaterialTheme.typography.titleMedium)
            }""", """            Button(
                onClick = { authenticateWithBiometrics() },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp),
                shape = unifiedShape,
                colors = ButtonDefaults.buttonColors(
                    containerColor = MaterialTheme.colorScheme.surfaceVariant, 
                    contentColor = androidx.compose.ui.graphics.Color(0xFFE0E0E0)
                )
            ) {
                Icon(Icons.Default.Fingerprint, contentDescription = "Biometrics", modifier = Modifier.size(20.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text("Unlock with Biometrics", style = MaterialTheme.typography.titleMedium)
            }""")

with open("app/src/main/java/com/example/ui/screens/LoginScreen.kt", "w") as f:
    f.write(content)
