import re

with open('app/src/main/java/com/example/ui/screens/SettingsScreen.kt', 'r') as f:
    content = f.read()

# Remove from SettingsDailyScheduleScreen
old_toggle_pattern = r'''            ListItem\(\s*headlineContent = \{ Text\("Time Format"\) \},\s*supportingContent = \{ Text\("24-hour format or 12 hour AM/PM format"\) \},\s*leadingContent = \{ Icon\(androidx.compose.material.icons.Icons.Default.AccessTime, contentDescription = null\) \},\s*trailingContent = \{ \s*Row\(\s*modifier = Modifier\s*\.background\(MaterialTheme.colorScheme.surfaceVariant, androidx.compose.foundation.shape.RoundedCornerShape\(16.dp\)\)\s*\.padding\(4.dp\),\s*verticalAlignment = Alignment.CenterVertically\s*\) \{\s*Box\(\s*modifier = Modifier\s*\.clickable \{ viewModel.setUse24HourFormat\(false\) \}\s*\.background\(if \(!uiState.use24HourFormat\) MaterialTheme.colorScheme.primary else androidx.compose.ui.graphics.Color.Transparent, androidx.compose.foundation.shape.RoundedCornerShape\(12.dp\)\)\s*\.padding\(horizontal = 12.dp, vertical = 6.dp\)\s*\) \{\s*Text\("12", color = if \(!uiState.use24HourFormat\) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = androidx.compose.ui.text.font.FontWeight.Bold\)\s*\}\s*Box\(\s*modifier = Modifier\s*\.clickable \{ viewModel.setUse24HourFormat\(true\) \}\s*\.background\(if \(uiState.use24HourFormat\) MaterialTheme.colorScheme.primary else androidx.compose.ui.graphics.Color.Transparent, androidx.compose.foundation.shape.RoundedCornerShape\(12.dp\)\)\s*\.padding\(horizontal = 12.dp, vertical = 6.dp\)\s*\) \{\s*Text\("24", color = if \(uiState.use24HourFormat\) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = androidx.compose.ui.text.font.FontWeight.Bold\)\s*\}\s*\}\s*\}\s*\)'''
toggle_match = re.search(old_toggle_pattern, content)
if toggle_match:
    toggle_text = toggle_match.group(0)
    content = content.replace(toggle_text + '\n', '')
else:
    print("Toggle not found in daily schedule screen.")

# Add to SettingsFeatureScreen
# We'll insert it right before the Daily Schedule list item.
insert_target = '''            ListItem(
                headlineContent = { Text("Daily Schedule") },'''
content = content.replace(insert_target, toggle_text + '\n' + insert_target, 1)

with open('app/src/main/java/com/example/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(content)
