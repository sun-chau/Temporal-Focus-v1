import re
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Find the HorizontalPager and update it
pattern = r"HorizontalPager\(\n\s*state = pagerState,\n\s*pageSize = PageSize\.Fixed\(\(24 \* 60 \* 1\.5\)\.dp\),\n\s*modifier = Modifier\.fillMaxSize\(\)\n\s*\) \{ page ->"

repl = """HorizontalPager(
                    state = pagerState,
                    modifier = Modifier.fillMaxSize()
                ) { page ->"""
content = re.sub(pattern, repl, content)

# We need to wrap the contents of the page in a horizontalScroll.
# Currently, inside the HorizontalPager:
# Box(modifier = Modifier.fillMaxSize()) {
#     // Timeline Ruler
#     androidx.compose.foundation.layout.Box(modifier = Modifier) {
#         TimelineRuler(uiState.use24HourFormat)
#     }
#     // Canvas Body
#     ...

# Let's add a scroll state inside the page.
pattern2 = r"Box\(modifier = Modifier\.fillMaxSize\(\)\) \{"
repl2 = """val pageScrollState = rememberScrollState()
                    
                    // Automatically scroll to current time if this is today's page
                    LaunchedEffect(Unit) {
                        if (page == Int.MAX_VALUE / 2) {
                            val cal = Calendar.getInstance()
                            val currentMinutes = cal.get(Calendar.HOUR_OF_DAY) * 60 + cal.get(Calendar.MINUTE)
                            val xOffsetPx = with(density) { (currentMinutes * 1.5f).dp.toPx() }
                            val targetScroll = (xOffsetPx - screenWidthPx / 2f).toInt()
                            pageScrollState.scrollTo(maxOf(0, targetScroll))
                        }
                    }
                    
                    Box(modifier = Modifier.fillMaxSize().horizontalScroll(pageScrollState)) {"""

content = re.sub(pattern2, repl2, content)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
