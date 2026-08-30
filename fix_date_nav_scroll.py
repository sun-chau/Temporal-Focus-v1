with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

target = """    // Scroll to center when pagerState.currentPage changes
    LaunchedEffect(pagerState.currentPage) {
        val startOffset = -500
        val targetIndex = pagerState.currentPage - (50000) - startOffset
        if (targetIndex in 0..1000) {
            listState.animateScrollToItem(
                index = targetIndex,
                scrollOffset = -centerOffsetPx
            )
        }
    }"""

replacement = """    var isFirstLaunch by remember { mutableStateOf(true) }

    // Scroll to center when pagerState.currentPage changes
    LaunchedEffect(pagerState.currentPage) {
        val startOffset = -500
        val targetIndex = pagerState.currentPage - (50000) - startOffset
        if (targetIndex in 0..1000) {
            if (isFirstLaunch) {
                listState.scrollToItem(
                    index = targetIndex,
                    scrollOffset = -centerOffsetPx
                )
                isFirstLaunch = false
            } else {
                listState.animateScrollToItem(
                    index = targetIndex,
                    scrollOffset = -centerOffsetPx
                )
            }
        }
    }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
