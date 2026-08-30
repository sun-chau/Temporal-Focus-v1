import re

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

# Add a ThemeSwitch composable at the bottom
theme_switch = """
@Composable
fun ThemeSwitch(
    checked: Boolean,
    onCheckedChange: ((Boolean) -> Unit)?,
    modifier: Modifier = Modifier,
    enabled: Boolean = true
) {
    androidx.compose.material3.Switch(
        checked = checked,
        onCheckedChange = onCheckedChange,
        modifier = modifier,
        enabled = enabled,
        colors = androidx.compose.material3.SwitchDefaults.colors(
            checkedThumbColor = androidx.compose.material3.MaterialTheme.colorScheme.surface,
            checkedTrackColor = androidx.compose.material3.MaterialTheme.colorScheme.primary,
            checkedIconColor = androidx.compose.material3.MaterialTheme.colorScheme.primary,
            uncheckedThumbColor = androidx.compose.material3.MaterialTheme.colorScheme.onSurface,
            uncheckedTrackColor = androidx.compose.material3.MaterialTheme.colorScheme.surfaceVariant,
            uncheckedIconColor = androidx.compose.material3.MaterialTheme.colorScheme.surface
        ),
        thumbContent = if (checked) {
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
    )
}
"""

if "fun ThemeSwitch(" not in content:
    content += theme_switch

# Replace Switch with ThemeSwitch
content = re.sub(r'\bSwitch\(', 'ThemeSwitch(', content)

# But we need to make sure we don't have multiple imports of Icons.Filled.Check or just use the fully qualified name like I did.

# Remove the In-App Notifications item
in_app_item_pattern = r'ListItem\(\s*headlineContent = \{ Text\("In-App Notifications \(Coming soon\)"[\s\S]*?\)\s*\},[\s\S]*?modifier = Modifier\.padding\(start = 16\.dp\)\.clickable \{ [^\}]+\} \}\s*\)'

content = re.sub(in_app_item_pattern, '', content)

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)
