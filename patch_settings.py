import re
with open('/app/applet/app/src/main/java/com/example/ui/screens/SettingsScreen.kt', 'r') as f:
    content = f.read()

# 1. Add alpha import
content = content.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\nimport androidx.compose.ui.draw.alpha")

# 2. Change 'Colour Customization Panel' to 'Theme and Color Customization'
content = content.replace('headlineContent = { Text("Colour Customization Panel") }', 'headlineContent = { Text("Theme and Color Customization") }')

# 3. Dim Notifications & Sounds
notifications_target = """            ListItem(
                headlineContent = { Text("Notifications & Sounds") },
                supportingContent = { Text("Tones and vibrations") },
                leadingContent = { Icon(Icons.Default.Notifications, contentDescription = null) },
                modifier = Modifier.clickable { viewModel.setTimerMode(com.example.viewmodel.TimerMode.SETTINGS_NOTIFICATIONS) }
            )"""
notifications_replacement = """            ListItem(
                headlineContent = { Text("Notifications & Sounds") },
                supportingContent = { Text("Tones and vibrations") },
                leadingContent = { Icon(Icons.Default.Notifications, contentDescription = null) },
                modifier = Modifier.alpha(0.5f)
            )"""
content = content.replace(notifications_target, notifications_replacement)

# 4. Modify SettingsSupportScreen
support_target = """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsSupportScreen(viewModel: MainViewModel, uiState: UiState, onBack: () -> Unit) {
    var showAboutDialog by remember { mutableStateOf(false) }
    var showFeedbackDialog by remember { mutableStateOf(false) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Support & About") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
        ) {
            ListItem(
                headlineContent = { Text("About") },
                supportingContent = { Text("App version and information") },
                leadingContent = { Icon(Icons.Default.Info, contentDescription = null) },
                modifier = Modifier.clickable { showAboutDialog = true }
            )
            ListItem(
                headlineContent = { Text("Update Logs") },
                supportingContent = { Text("View recent changes and updates") },
                leadingContent = { Icon(Icons.Default.History, contentDescription = null) },
                modifier = Modifier.clickable { viewModel.setTimerMode(com.example.viewmodel.TimerMode.UPDATE_LOG) }
            )
            ListItem(
                headlineContent = { Text("Help") },
                supportingContent = { Text("View help and documentation") },
                leadingContent = { Icon(Icons.AutoMirrored.Filled.HelpOutline, contentDescription = null) },
                modifier = Modifier.clickable {  }
            )
            ListItem(
                headlineContent = { Text("Feedback") },
                supportingContent = { Text("Send feedback and report issues") },
                leadingContent = { Icon(Icons.Default.Feedback, contentDescription = null) },
                modifier = Modifier.clickable { showFeedbackDialog = true }
            )
        }
    }

    if (showAboutDialog) {
        AlertDialog(
            onDismissRequest = { showAboutDialog = false },
            title = { Text("About Temporal Focus") },
            text = { Text("Version: ${com.example.BuildConfig.VERSION_NAME}\\n\\nA modern, minimalist productivity app designed to help you focus.") },
            confirmButton = {
                TextButton(onClick = { showAboutDialog = false }) {
                    Text("OK")
                }
            }
        )
    }

    if (showFeedbackDialog) {
        AlertDialog(
            onDismissRequest = { showFeedbackDialog = false },
            title = { Text("Feedback") },
            text = { Text("We appreciate your feedback! Please send your comments to support@example.com") },
            confirmButton = {
                TextButton(onClick = { showFeedbackDialog = false }) {
                    Text("Close")
                }
            }
        )
    }
}"""
support_replacement = """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsSupportScreen(viewModel: MainViewModel, uiState: UiState, onBack: () -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Support & About") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
        ) {
            ListItem(
                headlineContent = { Text("About") },
                supportingContent = { Text("App version and information") },
                leadingContent = { Icon(Icons.Default.Info, contentDescription = null) },
                modifier = Modifier.clickable { viewModel.setTimerMode(com.example.viewmodel.TimerMode.SETTINGS_ABOUT) }
            )
            ListItem(
                headlineContent = { Text("Update Logs") },
                supportingContent = { Text("View recent changes and updates") },
                leadingContent = { Icon(Icons.Default.History, contentDescription = null) },
                modifier = Modifier.clickable { viewModel.setTimerMode(com.example.viewmodel.TimerMode.UPDATE_LOG) }
            )
            ListItem(
                headlineContent = { Text("Help") },
                supportingContent = { Text("View help and documentation") },
                leadingContent = { Icon(Icons.AutoMirrored.Filled.HelpOutline, contentDescription = null) },
                modifier = Modifier.clickable { viewModel.setTimerMode(com.example.viewmodel.TimerMode.SETTINGS_HELP) }
            )
            ListItem(
                headlineContent = { Text("Feedback") },
                supportingContent = { Text("Send feedback and report issues") },
                leadingContent = { Icon(Icons.Default.Feedback, contentDescription = null) },
                modifier = Modifier.clickable { viewModel.setTimerMode(com.example.viewmodel.TimerMode.SETTINGS_FEEDBACK) }
            )
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsAboutScreen(onBack: () -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("About") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier.fillMaxSize().padding(padding),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Icon(Icons.Default.Info, contentDescription = null, modifier = Modifier.size(64.dp), tint = MaterialTheme.colorScheme.primary)
            Spacer(modifier = Modifier.height(16.dp))
            Text("Coming Soon", style = MaterialTheme.typography.titleLarge)
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsHelpScreen(onBack: () -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Help") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier.fillMaxSize().padding(padding),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Icon(Icons.AutoMirrored.Filled.HelpOutline, contentDescription = null, modifier = Modifier.size(64.dp), tint = MaterialTheme.colorScheme.primary)
            Spacer(modifier = Modifier.height(16.dp))
            Text("Coming Soon", style = MaterialTheme.typography.titleLarge)
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsFeedbackScreen(onBack: () -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Feedback") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier.fillMaxSize().padding(padding),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Icon(Icons.Default.Feedback, contentDescription = null, modifier = Modifier.size(64.dp), tint = MaterialTheme.colorScheme.primary)
            Spacer(modifier = Modifier.height(16.dp))
            Text("Coming Soon", style = MaterialTheme.typography.titleLarge)
        }
    }
}"""
content = content.replace(support_target, support_replacement)

with open('/app/applet/app/src/main/java/com/example/ui/screens/SettingsScreen.kt', 'w') as f:
    f.write(content)

