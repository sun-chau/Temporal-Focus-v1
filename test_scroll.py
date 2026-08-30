import re
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Make a shared state for Today's scroll
# Also a trigger to scroll back to now
shared_state = """    val todayScrollState = rememberScrollState()
    var scrollToNowTrigger by remember { mutableStateOf(0) }
    
    // Listen for scrollToNowTrigger to scroll today's scroll state
    LaunchedEffect(scrollToNowTrigger) {
        if (scrollToNowTrigger > 0) {
            val cal = Calendar.getInstance()
            val currentMinutes = cal.get(Calendar.HOUR_OF_DAY) * 60 + cal.get(Calendar.MINUTE)
            val xOffsetPx = with(density) { (currentMinutes * 1.5f).dp.toPx() }
            val screenWidthPx = with(density) { configuration.screenWidthDp.dp.toPx() }
            val targetScroll = (xOffsetPx - screenWidthPx / 2f).toInt()
            todayScrollState.animateScrollTo(maxOf(0, targetScroll))
            // Also ensure we are on today's page
            pagerState.animateScrollToPage(Int.MAX_VALUE / 2)
        }
    }
"""

content = content.replace("val verticalScrollState = rememberScrollState()", shared_state + "\n    val verticalScrollState = rememberScrollState()")

# Update the inside of the pager to use todayScrollState if page == Int.MAX_VALUE / 2
pattern = r"val pageScrollState = rememberScrollState\(\)\n\s*// Automatically scroll to current time if this is today's page\n\s*LaunchedEffect\(Unit\) \{\n\s*if \(page == Int\.MAX_VALUE / 2\) \{\n\s*val cal = Calendar\.getInstance\(\)\n\s*val currentMinutes = cal\.get\(Calendar\.HOUR_OF_DAY\) \* 60 \+ cal\.get\(Calendar\.MINUTE\)\n\s*val xOffsetPx = with\(density\) \{ \(currentMinutes \* 1\.5f\)\.dp\.toPx\(\) \}\n\s*val targetScroll = \(xOffsetPx - screenWidthPx / 2f\)\.toInt\(\)\n\s*pageScrollState\.scrollTo\(maxOf\(0, targetScroll\)\)\n\s*\}\n\s*\}"

repl = """val pageScrollState = if (page == Int.MAX_VALUE / 2) todayScrollState else rememberScrollState()
                    
                    // Automatically scroll to current time if this is today's page (initial load)
                    LaunchedEffect(Unit) {
                        if (page == Int.MAX_VALUE / 2 && scrollToNowTrigger == 0) {
                            val cal = Calendar.getInstance()
                            val currentMinutes = cal.get(Calendar.HOUR_OF_DAY) * 60 + cal.get(Calendar.MINUTE)
                            val xOffsetPx = with(density) { (currentMinutes * 1.5f).dp.toPx() }
                            val targetScroll = (xOffsetPx - screenWidthPx / 2f).toInt()
                            pageScrollState.scrollTo(maxOf(0, targetScroll))
                        }
                    }"""

content = re.sub(pattern, repl, content)

# Update Now button click handler
btn_pattern = r"coroutineScope\.launch \{\n\s*pagerState\.animateScrollToPage\(Int\.MAX_VALUE / 2\)\n\s*\}"
btn_repl = """coroutineScope.launch {
                                scrollToNowTrigger++
                            }"""
content = re.sub(btn_pattern, btn_repl, content)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
