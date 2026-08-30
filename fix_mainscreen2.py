with open("app/src/main/java/com/example/ui/screens/MainScreen.kt", "r") as f:
    content = f.read()

search = '''                    NavigationDrawerItem(
                        icon = { Icon(Icons.Outlined.Brightness4, contentDescription = null) },
                        label = { Text("Daily Schedule") },
                        selected = false,
                        onClick = {
                            scope.launch { drawerState.close() }
                            showDailyScheduleScreen = true
                        },'''
replace = '''                    NavigationDrawerItem(
                        icon = { Icon(if (uiState.currentMode == TimerMode.DAILY_SCHEDULE) Icons.Filled.DateRange else Icons.Outlined.DateRange, contentDescription = null) },
                        label = { Text("Daily Schedule") },
                        selected = uiState.currentMode == TimerMode.DAILY_SCHEDULE,
                        onClick = {
                            viewModel.setTimerMode(TimerMode.DAILY_SCHEDULE)
                            scope.launch { drawerState.close() }
                        },'''
content = content.replace(search, replace)
with open("app/src/main/java/com/example/ui/screens/MainScreen.kt", "w") as f:
    f.write(content)
