import re
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Add a state for NowButton visibility
state_decl = """    var showDatePicker by remember { mutableStateOf(false) }
    var isNowLineVisible by remember { mutableStateOf(true) }"""
content = re.sub(r"var showDatePicker by remember \{ mutableStateOf\(false\) \}", state_decl, content)

# Modify NowLine to detect visibility
now_line_pattern = r"if \(isToday\) \{\n\s*NowLine\(\)\n\s*\}"
now_line_repl = """if (isToday) {
                            val cal = Calendar.getInstance()
                            val currentMinutes = cal.get(Calendar.HOUR_OF_DAY) * 60 + cal.get(Calendar.MINUTE)
                            val xOffset = (currentMinutes * 1.5f).dp
                            
                            Box(
                                modifier = Modifier
                                    .offset(x = xOffset)
                                    .width(2.dp)
                                    .fillMaxHeight()
                                    .background(Color.Red)
                                    .androidx.compose.ui.layout.onGloballyPositioned { coordinates ->
                                        val windowBounds = coordinates.boundsInWindow()
                                        isNowLineVisible = windowBounds.right > 0 && windowBounds.left < screenWidthPx
                                    }
                            )
                        }"""
content = re.sub(now_line_pattern, now_line_repl, content)

# Add screenWidthPx calculation
density_pattern = r"val density = LocalDensity\.current\n\s*val configuration = LocalConfiguration\.current"
density_repl = """val density = LocalDensity.current
    val configuration = LocalConfiguration.current
    val screenWidthPx = with(density) { configuration.screenWidthDp.dp.toPx() }"""
content = re.sub(density_pattern, density_repl, content)

# Update FloatingActionButton to a Column containing Now button and Add button
fab_pattern = r"floatingActionButton = \{\n\s*FloatingActionButton\(onClick = \{\s*viewModel\.clearDailyScheduleDraft\(\)\s*viewModel\.setTimerMode\(com\.example\.viewmodel\.TimerMode\.CREATE_DAILY_SCHEDULE\)\s*\}, containerColor = MaterialTheme\.colorScheme\.primary, contentColor = MaterialTheme\.colorScheme\.background\) \{\n\s*Icon\(Icons\.Default\.Add, contentDescription = \"Add Schedule\"\)\n\s*\}\n\s*\},"
fab_repl = """floatingActionButton = {
            Column(horizontalAlignment = Alignment.End, verticalArrangement = Arrangement.spacedBy(16.dp)) {
                androidx.compose.animation.AnimatedVisibility(
                    visible = !isNowLineVisible,
                    enter = androidx.compose.animation.fadeIn() + androidx.compose.animation.scaleIn(),
                    exit = androidx.compose.animation.fadeOut() + androidx.compose.animation.scaleOut()
                ) {
                    FloatingActionButton(
                        onClick = { 
                            // We can't scroll to a specific pixel in HorizontalPager directly if it snaps, 
                            // but we can scroll to the page. 
                            coroutineScope.launch {
                                pagerState.animateScrollToPage(Int.MAX_VALUE / 2)
                            }
                        },
                        containerColor = MaterialTheme.colorScheme.secondaryContainer,
                        contentColor = MaterialTheme.colorScheme.onSecondaryContainer
                    ) {
                        Icon(androidx.compose.material.icons.Icons.Default.LocationSearching, contentDescription = "Now")
                    }
                }
                FloatingActionButton(onClick = { 
                    viewModel.clearDailyScheduleDraft()
                    viewModel.setTimerMode(com.example.viewmodel.TimerMode.CREATE_DAILY_SCHEDULE)
                }, containerColor = MaterialTheme.colorScheme.primary, contentColor = MaterialTheme.colorScheme.background) {
                    Icon(Icons.Default.Add, contentDescription = "Add Schedule")
                }
            }
        },"""
content = re.sub(fab_pattern, fab_repl, content)

# Remove the old NowLine function definition to avoid unused/unresolved references
content = re.sub(r"@Composable\nfun NowLine\(\) \{[\s\S]*?\n\}\n", "", content)

# Also need to import LocationSearching, boundsInWindow
content = content.replace("import androidx.compose.material.icons.filled.Today", "import androidx.compose.material.icons.filled.Today\nimport androidx.compose.material.icons.filled.LocationSearching\nimport androidx.compose.ui.layout.boundsInWindow")

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
