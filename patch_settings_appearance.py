import re
with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

new_item = """            ListItem(
                headlineContent = { Text("Launcher Icon") },
                supportingContent = { Text("Tap to set the home screen icon color.") },
                trailingContent = { Icon(Icons.AutoMirrored.Filled.KeyboardArrowRight, contentDescription = null) },
                modifier = Modifier.clickable { viewModel.setTimerMode(com.example.viewmodel.TimerMode.SETTINGS_LAUNCHER_ICON) }
            )"""

content = content.replace("headlineContent = { Text(\"Colour Customization Panel\") },", new_item + "\n            ListItem(\n                headlineContent = { Text(\"Colour Customization Panel\") },")

new_screen = """
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LauncherIconScreen(viewModel: MainViewModel, uiState: UiState, onBack: () -> Unit) {
    val context = androidx.compose.ui.platform.LocalContext.current
    var pendingIcon by remember { mutableStateOf<String?>(null) }
    
    val themes = listOf(
        "orange" to "Baseline/Default",
        "obsidian" to "Obsidian Dark",
        "daylight" to "Daylight Clear",
        "midnight" to "Midnight Minimalist",
        "nordic" to "Nordic Frost",
        "forest" to "Forest Canopy",
        "crimson" to "Crimson Twilight",
        "amber" to "Amber Glow",
        "monochrome" to "Monochrome"
    )
    
    val icons = mapOf(
        "orange" to com.example.R.mipmap.ic_launcher_orange,
        "obsidian" to com.example.R.mipmap.ic_launcher_obsidian,
        "daylight" to com.example.R.mipmap.ic_launcher_daylight,
        "midnight" to com.example.R.mipmap.ic_launcher_midnight,
        "nordic" to com.example.R.mipmap.ic_launcher_nordic,
        "forest" to com.example.R.mipmap.ic_launcher_forest,
        "crimson" to com.example.R.mipmap.ic_launcher_crimson,
        "amber" to com.example.R.mipmap.ic_launcher_amber,
        "monochrome" to com.example.R.mipmap.ic_launcher_monochrome
    )

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Launcher Icon") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        androidx.compose.foundation.lazy.grid.LazyVerticalGrid(
            columns = androidx.compose.foundation.lazy.grid.GridCells.Fixed(3),
            contentPadding = PaddingValues(16.dp),
            modifier = Modifier.fillMaxSize().padding(padding)
        ) {
            items(themes.size) { index ->
                val (id, name) = themes[index]
                val isActive = uiState.launcherIcon == id
                
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier
                        .padding(8.dp)
                        .clickable {
                            if (!isActive) {
                                pendingIcon = id
                            }
                        }
                ) {
                    Box(
                        modifier = Modifier
                            .size(72.dp)
                            .androidx.compose.foundation.background(
                                color = if (isActive) MaterialTheme.colorScheme.primaryContainer else androidx.compose.ui.graphics.Color.Transparent,
                                shape = androidx.compose.foundation.shape.RoundedCornerShape(16.dp)
                            )
                            .padding(4.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        androidx.compose.foundation.Image(
                            painter = androidx.compose.ui.res.painterResource(id = icons[id] ?: com.example.R.mipmap.ic_launcher),
                            contentDescription = name,
                            modifier = Modifier.size(64.dp)
                        )
                        if (isActive) {
                            Icon(
                                Icons.Default.CheckCircle,
                                contentDescription = "Active",
                                tint = MaterialTheme.colorScheme.primary,
                                modifier = Modifier.align(Alignment.BottomEnd).size(24.dp).androidx.compose.foundation.background(androidx.compose.ui.graphics.Color.White, androidx.compose.foundation.shape.CircleShape)
                            )
                        }
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = name,
                        style = MaterialTheme.typography.bodySmall,
                        textAlign = androidx.compose.ui.text.style.TextAlign.Center,
                        maxLines = 2
                    )
                }
            }
        }
    }
    
    if (pendingIcon != null) {
        AlertDialog(
            onDismissRequest = { pendingIcon = null },
            title = { Text("Change Launcher Icon") },
            text = { Text("Changing the home screen icon will briefly restart the launcher. Are you sure you want to apply the ${themes.find { it.first == pendingIcon }?.second} icon?") },
            confirmButton = {
                TextButton(
                    onClick = {
                        val iconId = pendingIcon!!
                        pendingIcon = null
                        
                        viewModel.setLauncherIcon(iconId)
                        
                        val pm = context.packageManager
                        val packageName = context.packageName
                        
                        val allAliases = listOf(
                            "MainActivityOrange",
                            "MainActivityObsidian",
                            "MainActivityDaylight",
                            "MainActivityMidnight",
                            "MainActivityNordic",
                            "MainActivityForest",
                            "MainActivityCrimson",
                            "MainActivityAmber",
                            "MainActivityMonochrome"
                        )
                        
                        val targetAlias = "MainActivity" + iconId.replaceFirstChar { it.uppercase() }
                        
                        for (alias in allAliases) {
                            val componentName = android.content.ComponentName(packageName, "$packageName.$alias")
                            pm.setComponentEnabledSetting(
                                componentName,
                                if (alias == targetAlias) android.content.pm.PackageManager.COMPONENT_ENABLED_STATE_ENABLED else android.content.pm.PackageManager.COMPONENT_ENABLED_STATE_DISABLED,
                                android.content.pm.PackageManager.DONT_KILL_APP
                            )
                        }
                        
                        // Disable the main default activity as well, unless orange is selected
                        // Wait, if orange is selected, we enable MainActivityOrange. So MainActivity can be disabled?
                        // If we disable MainActivity, we MUST have an enabled alias.
                        // Actually, it's safer to always leave MainActivity enabled and just use it as default?
                        // No, if MainActivity is enabled and an alias is enabled, we get two icons.
                        // So we MUST disable MainActivity if we use an alias.
                        val mainActivity = android.content.ComponentName(packageName, "$packageName.MainActivity")
                        pm.setComponentEnabledSetting(
                            mainActivity,
                            android.content.pm.PackageManager.COMPONENT_ENABLED_STATE_DISABLED,
                            android.content.pm.PackageManager.DONT_KILL_APP
                        )
                    }
                ) {
                    Text("Apply")
                }
            },
            dismissButton = {
                TextButton(onClick = { pendingIcon = null }) {
                    Text("Cancel")
                }
            }
        )
    }
}
"""

content = content + "\n" + new_screen

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)
