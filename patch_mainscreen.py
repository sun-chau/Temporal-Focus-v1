import re

with open("app/src/main/java/com/example/ui/screens/MainScreen.kt", "r") as f:
    content = f.read()

# 1. Drawer Sheet Geometry
target_drawer = """            ModalDrawerSheet(
                drawerContainerColor = MaterialTheme.colorScheme.surface,
                drawerShape = RoundedCornerShape(topEnd = 16.dp, bottomEnd = 16.dp)
            )"""
replacement_drawer = """            ModalDrawerSheet(
                modifier = Modifier.border(1.dp, MaterialTheme.colorScheme.outlineVariant, RectangleShape),
                drawerContainerColor = MaterialTheme.colorScheme.surface,
                drawerShape = RectangleShape
            )"""
content = content.replace(target_drawer, replacement_drawer)

# 2. Profile Header Hardening
target_profile_image = """                                    .border(1.dp, MaterialTheme.colorScheme.primary, CircleShape)
                                    .padding(6.dp)
                            ) {
                                coil.compose.AsyncImage(
                                    model = coil.request.ImageRequest.Builder(context)
                                        .data(uiState.profileImageUri)
                                        .crossfade(true)
                                        .build(),
                                    contentDescription = "Profile",
                                    contentScale = androidx.compose.ui.layout.ContentScale.Crop,
                                    modifier = Modifier
                                        .fillMaxSize()
                                        .clip(CircleShape)
                                )"""
replacement_profile_image = """                                    .border(1.dp, MaterialTheme.colorScheme.primary, RectangleShape)
                                    .padding(6.dp)
                            ) {
                                coil.compose.AsyncImage(
                                    model = coil.request.ImageRequest.Builder(context)
                                        .data(uiState.profileImageUri)
                                        .crossfade(true)
                                        .build(),
                                    contentDescription = "Profile",
                                    contentScale = androidx.compose.ui.layout.ContentScale.Crop,
                                    modifier = Modifier
                                        .fillMaxSize()
                                        .clip(RectangleShape)
                                )"""
content = content.replace(target_profile_image, replacement_profile_image)

target_profile_icon = """                                    .border(1.dp, MaterialTheme.colorScheme.primary, CircleShape)
                                    .padding(6.dp)
                            ) {
                                Box(
                                    modifier = Modifier
                                        .fillMaxSize()
                                        .clip(CircleShape)
                                        .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.2f)),"""
replacement_profile_icon = """                                    .border(1.dp, MaterialTheme.colorScheme.primary, RectangleShape)
                                    .padding(6.dp)
                            ) {
                                Box(
                                    modifier = Modifier
                                        .fillMaxSize()
                                        .clip(RectangleShape)
                                        .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.2f)),"""
content = content.replace(target_profile_icon, replacement_profile_icon)

target_greeting = """                            Text(
                                text = "Hi, ${uiState.profileName.takeIf { it.isNotBlank() } ?: "Guest"}",
                                style = MaterialTheme.typography.headlineMedium,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.onSurface,
                                maxLines = 1,
                                overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
                            )"""
replacement_greeting = """                            Text(
                                text = "[ AUTH: ${uiState.profileName.takeIf { it.isNotBlank() }?.uppercase(java.util.Locale.getDefault()) ?: "GUEST"} ]",
                                fontFamily = FontFamily.Monospace,
                                style = MaterialTheme.typography.headlineSmall,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.onSurface,
                                maxLines = 1,
                                overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
                            )"""
content = content.replace(target_greeting, replacement_greeting)

# 3. Navigation Command List
# Replace shape
content = content.replace("shape = RoundedCornerShape(50),", "shape = RectangleShape,")

# Replace labels dynamically
def label_replacer(match):
    text = match.group(1)
    return f'label = {{ Text("{text.upper()}", fontFamily = FontFamily.Monospace) }}'

content = re.sub(r'label = \{ Text\("([^"]+)"\) \}', label_replacer, content)

# Replace colors
target_colors = """                        colors = NavigationDrawerItemDefaults.colors(
                            selectedContainerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.15f),
                            unselectedContainerColor = Color.Transparent,
                            selectedIconColor = MaterialTheme.colorScheme.primary,
                            selectedTextColor = MaterialTheme.colorScheme.primary,
                            unselectedIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
                            unselectedTextColor = MaterialTheme.colorScheme.onSurfaceVariant
                        ),"""
replacement_colors = """                        colors = NavigationDrawerItemDefaults.colors(
                            selectedContainerColor = MaterialTheme.colorScheme.primary,
                            unselectedContainerColor = Color.Transparent,
                            selectedIconColor = MaterialTheme.colorScheme.onPrimary,
                            selectedTextColor = MaterialTheme.colorScheme.onPrimary,
                            unselectedIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
                            unselectedTextColor = MaterialTheme.colorScheme.onSurfaceVariant
                        ),"""
content = content.replace(target_colors, replacement_colors)

# 4. Mechanical Dividers
content = content.replace("HorizontalDivider(color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.05f))", "HorizontalDivider(color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.2f))")
content = content.replace("HorizontalDivider(modifier = Modifier.padding(horizontal = 28.dp), color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.05f))", "HorizontalDivider(modifier = Modifier.padding(horizontal = 28.dp), color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.2f))")

with open("app/src/main/java/com/example/ui/screens/MainScreen.kt", "w") as f:
    f.write(content)

print("MainScreen patched")
