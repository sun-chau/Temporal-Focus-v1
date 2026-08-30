path = 'app/src/main/java/com/example/ui/screens/MainScreen.kt'
with open(path, 'r') as f:
    content = f.read()

# 1. Update Drawer Container Color
content = content.replace(
    "drawerContainerColor = MaterialTheme.colorScheme.surfaceColorAtElevation(1.dp),",
    "drawerContainerColor = MaterialTheme.colorScheme.surface,"
)

# 2. Update Header background
content = content.replace(
    ".background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))",
    ".background(MaterialTheme.colorScheme.primary.copy(alpha = 0.08f))"
)

# 3. Update NavigationDrawerItem styling
drawer_item_colors = """shape = RoundedCornerShape(50),
                        colors = NavigationDrawerItemDefaults.colors(
                            selectedContainerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.15f),
                            unselectedContainerColor = Color.Transparent,
                            selectedIconColor = MaterialTheme.colorScheme.primary,
                            selectedTextColor = MaterialTheme.colorScheme.primary,
                            unselectedIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
                            unselectedTextColor = MaterialTheme.colorScheme.onSurfaceVariant
                        ),"""

content = content.replace("shape = RoundedCornerShape(50),", drawer_item_colors)

with open(path, 'w') as f:
    f.write(content)
print("Updated drawer styles.")
