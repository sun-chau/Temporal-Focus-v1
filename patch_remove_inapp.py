import re

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

# Try to find the list item containing "In-App Notifications (Coming soon)" and remove it.
# We will just find the block from ListItem to the end of the clickable modifier.
start_str = '            val context = LocalContext.current'
end_str = '            ListItem(\n                headlineContent = { Text("Notification Offset'

if start_str in content and end_str in content:
    idx_start = content.find(start_str)
    idx_end = content.find(end_str)
    
    # Let's remove from idx_start to idx_end
    content = content[:idx_start] + "            val context = LocalContext.current\n" + content[idx_end:]

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)

