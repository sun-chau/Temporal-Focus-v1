import re
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Replace selectedDateMillis state with pagerState
pattern = r"var selectedDateMillis by remember \{ mutableStateOf\(getStartOfDayMillis\(System\.currentTimeMillis\(\)\)\) \}"
replacement = """val pagerState = rememberPagerState(initialPage = Int.MAX_VALUE / 2, pageCount = { Int.MAX_VALUE })
    val todayMillis = getStartOfDayMillis(System.currentTimeMillis())
    val dayOffset = pagerState.currentPage - (Int.MAX_VALUE / 2)
    val selectedDateMillis = todayMillis + dayOffset * 24 * 60 * 60 * 1000L
    
    var showDatePicker by remember { mutableStateOf(false) }"""
content = re.sub(pattern, replacement, content)

# TopAppBar actions
appbar_pattern = r"title = \{ Text\(\"Daily Schedule\"\) \},\n\s*navigationIcon = \{\n\s*IconButton\(onClick = onMenuClick\) \{\n\s*Icon\(Icons\.Default\.Menu, contentDescription = \"Menu\"\)\n\s*\}\n\s*\},"
appbar_repl = """title = { Text("Daily Schedule") },
                navigationIcon = {
                    IconButton(onClick = onMenuClick) {
                        Icon(Icons.Default.Menu, contentDescription = "Menu")
                    }
                },
                actions = {
                    IconButton(onClick = { 
                        coroutineScope.launch {
                            pagerState.animateScrollToPage(Int.MAX_VALUE / 2)
                        }
                    }) {
                        Icon(androidx.compose.material.icons.Icons.Default.Today, contentDescription = "Today")
                    }
                    IconButton(onClick = { showDatePicker = true }) {
                        Icon(Icons.Default.DateRange, contentDescription = "Calendar")
                    }
                },"""
content = re.sub(appbar_pattern, appbar_repl, content)

# Remove horizontalScrollState
content = re.sub(r"val horizontalScrollState = rememberScrollState\(\)\n", "", content)

# Replace Column and horizontalScroll with HorizontalPager
pager_pattern = r"Column\(\n\s*modifier = Modifier\n\s*\.fillMaxSize\(\)\n\s*\.horizontalScroll\(horizontalScrollState\)\n\s*\) \{"
pager_repl = """HorizontalPager(
                    state = pagerState,
                    pageSize = PageSize.Fixed((24 * 60 * 1.5).dp),
                    modifier = Modifier.fillMaxSize()
                ) { page ->
                    val pageDayOffset = page - (Int.MAX_VALUE / 2)
                    val pageDateMillis = todayMillis + pageDayOffset * 24 * 60 * 60 * 1000L
                    val startOfDay = pageDateMillis
                    val endOfDay = pageDateMillis + 24 * 60 * 60 * 1000L - 1L
                    val schedulesForDate = uiState.dailySchedules.filter {
                        it.startTime <= endOfDay && it.endTime > startOfDay
                    }.sortedBy { it.startTime }
                    
                    Box(modifier = Modifier.fillMaxSize()) {"""
content = re.sub(pager_pattern, pager_repl, content)

# Find the closing brace of the Column (now HorizontalPager wrapper) and add the dashed lines
# Since we replaced the Column with HorizontalPager + Box, we have one extra closing brace needed or we can just append the dashed lines inside the Box.
dashed_lines = """
                        // Boundary lines
                        androidx.compose.foundation.layout.Box(
                            modifier = Modifier
                                .fillMaxHeight()
                                .width(1.dp)
                                .align(Alignment.CenterStart)
                                .background(MaterialTheme.colorScheme.outlineVariant)
                        )
                        Text(
                            text = "Midnight",
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.outlineVariant,
                            modifier = Modifier.align(Alignment.TopStart).padding(start = 4.dp, top = 4.dp)
                        )
                        
                        androidx.compose.foundation.layout.Box(
                            modifier = Modifier
                                .fillMaxHeight()
                                .width(1.dp)
                                .align(Alignment.CenterEnd)
                                .background(MaterialTheme.colorScheme.outlineVariant)
                        )
                        Text(
                            text = "Midnight",
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.outlineVariant,
                            modifier = Modifier.align(Alignment.TopEnd).padding(end = 4.dp, top = 4.dp)
                        )
                    }"""

# We need to replace the closing brace of the Column with `dashed_lines` + `}`
# Actually, the original code had:
# 151                Column(
# ...
# 165                        .width((24 * 60 * 1.5).dp)
# 166                ) {
# ...
# 276                }
# 277            }
# 278    }
# Let's write a targeted script to do this properly.
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
