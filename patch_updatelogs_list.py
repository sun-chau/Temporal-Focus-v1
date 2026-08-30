with open('/app/applet/app/src/main/java/com/example/ui/screens/UpdateLogScreen.kt', 'r') as f:
    lines = f.readlines()

new_lines = lines[:31] # lines 1 to 31
new_lines.append("""val updateLogs = listOf(
    UpdateLogEntry(
        timestamp = "27.08.2026.15.30",
        added = listOf("Added new Settings menus", "Prepared Developer Mode pages"),
        changed = listOf("Renamed Colour Customization Panel", "Dimmed Notifications & Settings"),
        fixed = emptyList(),
        removed = emptyList()
    )
)
""")
new_lines.extend(lines[159:]) # From line 160 onwards

with open('/app/applet/app/src/main/java/com/example/ui/screens/UpdateLogScreen.kt', 'w') as f:
    f.writelines(new_lines)

