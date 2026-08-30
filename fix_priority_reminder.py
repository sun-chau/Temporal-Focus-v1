import re

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "r") as f:
    content = f.read()

search_str = r'''                Row\(modifier = Modifier\.fillMaxWidth\(\), horizontalArrangement = Arrangement\.SpaceBetween\) \{
                    val recurringOptions = listOf\("Daily", "Weekly", "Monthly", "Annually", "Custom"\)'''

replace_str = '''                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    val context = LocalContext.current
                    OutlinedButton(
                        onClick = { android.widget.Toast.makeText(context, "Coming soon", android.widget.Toast.LENGTH_SHORT).show() },
                        modifier = Modifier.weight(1f).height(48.dp),
                        shape = RoundedCornerShape(12.dp),
                        colors = ButtonDefaults.outlinedButtonColors(contentColor = Color.Gray),
                        border = androidx.compose.foundation.BorderStroke(1.dp, Color.White.copy(alpha = 0.2f))
                    ) {
                        Icon(Icons.Outlined.Info, contentDescription = "Priority", modifier = Modifier.size(16.dp))
                        Spacer(Modifier.width(8.dp))
                        Text("Priority")
                    }
                    OutlinedButton(
                        onClick = { android.widget.Toast.makeText(context, "Coming soon", android.widget.Toast.LENGTH_SHORT).show() },
                        modifier = Modifier.weight(1f).height(48.dp),
                        shape = RoundedCornerShape(12.dp),
                        colors = ButtonDefaults.outlinedButtonColors(contentColor = Color.Gray),
                        border = androidx.compose.foundation.BorderStroke(1.dp, Color.White.copy(alpha = 0.2f))
                    ) {
                        Icon(Icons.Outlined.Notifications, contentDescription = "Reminder", modifier = Modifier.size(16.dp))
                        Spacer(Modifier.width(8.dp))
                        Text("Reminder")
                    }
                }
                
                Spacer(Modifier.height(20.dp))
                
                // Recurring
                Text("RECURRING", color = Color.Gray, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(8.dp))
                
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    val recurringOptions = listOf("Daily", "Weekly", "Monthly", "Annually", "Custom")'''

content = re.sub(search_str, replace_str, content)

if "import androidx.compose.material.icons.outlined.Notifications" not in content:
    content = content.replace("import androidx.compose.material.icons.outlined.Info", "import androidx.compose.material.icons.outlined.Info\nimport androidx.compose.material.icons.outlined.Notifications")

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "w") as f:
    f.write(content)
