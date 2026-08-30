import re
with open('/app/applet/app/src/main/java/com/example/ui/screens/UpdateLogScreen.kt', 'r') as f:
    content = f.read()

# Replace the entire updateLogs list with a dummy list
target_list = re.search(r"val updateLogs = listOf\(.*?\)\)\n\n@OptIn", content, re.DOTALL)
if target_list:
    replacement_list = """val updateLogs = listOf(
    UpdateLogEntry(
        timestamp = "27.08.2026.15.30",
        added = listOf("Added new Settings menus", "Prepared Developer Mode pages"),
        changed = listOf("Renamed Colour Customization Panel", "Dimmed Notifications & Settings"),
        fixed = emptyList(),
        removed = emptyList()
    )
)

@OptIn"""
    content = content.replace(target_list.group(0), replacement_list)
else:
    print("Could not find updateLogs list")

# Replace UpdateLogCard with an expandable version
target_card = re.search(r"@Composable\nfun UpdateLogCard\(log: UpdateLogEntry\) \{.*?^\}", content, re.DOTALL | re.MULTILINE)
if target_card:
    replacement_card = """@Composable
fun UpdateLogCard(log: UpdateLogEntry) {
    var expanded by remember { mutableStateOf(false) }
    Card(
        modifier = Modifier.fillMaxWidth().clickable { expanded = !expanded },
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f))
    ) {
        Column(modifier = Modifier.fillMaxWidth().padding(16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = log.timestamp,
                    fontWeight = FontWeight.Bold,
                    fontSize = 16.sp,
                    color = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.weight(1f)
                )
                Icon(
                    imageVector = if (expanded) Icons.Default.ExpandLess else Icons.Default.ExpandMore,
                    contentDescription = if (expanded) "Collapse" else "Expand",
                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            
            AnimatedVisibility(visible = expanded) {
                Column(modifier = Modifier.padding(top = 12.dp)) {
                    if (log.added.isNotEmpty()) {
                        LogSection("Added", log.added, MaterialTheme.colorScheme.tertiary)
                    }
                    if (log.changed.isNotEmpty()) {
                        LogSection("Changed", log.changed, MaterialTheme.colorScheme.secondary)
                    }
                    if (log.fixed.isNotEmpty()) {
                        LogSection("Fixed", log.fixed, MaterialTheme.colorScheme.primary)
                    }
                    if (log.removed.isNotEmpty()) {
                        LogSection("Removed", log.removed, MaterialTheme.colorScheme.error)
                    }
                }
            }
        }
    }
}"""
    content = content.replace(target_card.group(0), replacement_card)
else:
    print("Could not find UpdateLogCard")

# Make sure imports are there for expandable card
if "import androidx.compose.animation.AnimatedVisibility" not in content:
    content = content.replace("import androidx.compose.ui.unit.sp", "import androidx.compose.ui.unit.sp\nimport androidx.compose.animation.AnimatedVisibility\nimport androidx.compose.foundation.clickable\nimport androidx.compose.runtime.getValue\nimport androidx.compose.runtime.setValue\nimport androidx.compose.runtime.remember\nimport androidx.compose.runtime.mutableStateOf")

with open('/app/applet/app/src/main/java/com/example/ui/screens/UpdateLogScreen.kt', 'w') as f:
    f.write(content)
