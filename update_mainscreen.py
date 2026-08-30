import re

with open('app/src/main/java/com/example/ui/screens/MainScreen.kt', 'r') as f:
    content = f.read()

# 1. Add drawer item
pomodoro_drawer_item = """                        modifier = Modifier.padding(NavigationDrawerItemDefaults.ItemPadding)
                    )"""

quick_deadlines_drawer_item = """                        modifier = Modifier.padding(NavigationDrawerItemDefaults.ItemPadding)
                    )
                    
                    NavigationDrawerItem(
                        icon = { Icon(if (uiState.currentMode == TimerMode.QUICK_DEADLINES) Icons.Filled.AccessTime else Icons.Outlined.AccessTime, contentDescription = null) },
                        label = { Text("Quick Deadlines") },
                        selected = uiState.currentMode == TimerMode.QUICK_DEADLINES,
                        onClick = {
                            viewModel.setTimerMode(TimerMode.QUICK_DEADLINES)
                            scope.launch { drawerState.close() }
                        },
                        shape = RoundedCornerShape(50),
                        colors = NavigationDrawerItemDefaults.colors(
                            selectedContainerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.15f),
                            unselectedContainerColor = Color.Transparent,
                            selectedIconColor = MaterialTheme.colorScheme.primary,
                            selectedTextColor = MaterialTheme.colorScheme.primary,
                            unselectedIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
                            unselectedTextColor = MaterialTheme.colorScheme.onSurfaceVariant
                        ),
                        modifier = Modifier.padding(NavigationDrawerItemDefaults.ItemPadding)
                    )"""

# Only replace the first occurrence after POMODORO
# POMODORO drawer item is around lines 269-281
parts = content.split('label = { Text("Pomodoro") },')
if len(parts) > 1:
    sub_parts = parts[1].split('modifier = Modifier.padding(NavigationDrawerItemDefaults.ItemPadding)\n                    )', 1)
    if len(sub_parts) > 1:
        parts[1] = sub_parts[0] + quick_deadlines_drawer_item + sub_parts[1]
    content = 'label = { Text("Pomodoro") },'.join(parts)


# 2. Add route for QUICK_DEADLINES
route = """                            TimerMode.POMODORO -> PomodoroScreen(viewModel, uiState, onMenuClick = { scope.launch { drawerState.open() } })"""
new_route = route + """\n                            TimerMode.QUICK_DEADLINES -> QuickDeadlinesScreen(viewModel, uiState, onMenuClick = { scope.launch { drawerState.open() } })"""
content = content.replace(route, new_route)


# 3. Remove QuickDeadlineSheet
sheet_code = """    if (uiState.showQuickDeadlineSheet) {
        com.example.ui.components.QuickDeadlineSheet(
            onDismiss = { viewModel.setQuickDeadlineSheet(false) },
            onSave = { name, time -> viewModel.addQuickDeadline(name, time) }
        )
    }"""
content = content.replace(sheet_code, "")

# Remove Icons.Filled.AccessTime / Icons.Outlined.AccessTime import if not exists, but we can just import it
import_stmt = "import androidx.compose.material.icons.outlined.AccessTime\nimport androidx.compose.material.icons.filled.AccessTime"
content = content.replace("import androidx.compose.material.icons.Icons", "import androidx.compose.material.icons.Icons\n" + import_stmt)

with open('app/src/main/java/com/example/ui/screens/MainScreen.kt', 'w') as f:
    f.write(content)

