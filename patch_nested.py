import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

target = """                                        // Automatically scroll to current time if this is today's page (initial load)
                    LaunchedEffect(Unit) {
                        if (page == 50000 && scrollToNowTrigger == 0) {
                            val cal = Calendar.getInstance()
                            val currentMinutes = cal.get(Calendar.HOUR_OF_DAY) * 60 + cal.get(Calendar.MINUTE)
                            val xOffsetPx = with(density) { (currentMinutes * 1.5f).dp.toPx() }
                            val targetScroll = (xOffsetPx - screenWidthPx / 2f).toInt()
                            pageScrollState.scrollTo(maxOf(0, targetScroll))
                        }
                    }
                    
                    Box(modifier = Modifier.fillMaxSize().horizontalScroll(pageScrollState)) {"""

replacement = """                                        // Automatically scroll to current time if this is today's page (initial load)
                    LaunchedEffect(Unit) {
                        if (page == 50000 && scrollToNowTrigger == 0) {
                            val cal = Calendar.getInstance()
                            val currentMinutes = cal.get(Calendar.HOUR_OF_DAY) * 60 + cal.get(Calendar.MINUTE)
                            val xOffsetPx = with(density) { (currentMinutes * 1.5f).dp.toPx() }
                            val targetScroll = (xOffsetPx - screenWidthPx / 2f).toInt()
                            pageScrollState.scrollTo(maxOf(0, targetScroll))
                        }
                    }
                    
                    val nestedScrollConnection = remember(pageScrollState) {
                        object : androidx.compose.ui.input.nestedscroll.NestedScrollConnection {
                            override fun onPreScroll(
                                available: androidx.compose.ui.geometry.Offset,
                                source: androidx.compose.ui.input.nestedscroll.NestedScrollSource
                            ): androidx.compose.ui.geometry.Offset {
                                val canScrollForward = pageScrollState.value < pageScrollState.maxValue
                                val canScrollBackward = pageScrollState.value > 0
                                
                                val tryingToPanBackward = available.x > 0
                                val tryingToPanForward = available.x < 0
                                
                                if ((tryingToPanBackward && !canScrollBackward) || (tryingToPanForward && !canScrollForward)) {
                                    // By not consuming, we allow horizontalScroll to receive it. 
                                    // But since horizontalScroll has no room, it will pass it to onPostScroll.
                                    return androidx.compose.ui.geometry.Offset.Zero
                                }
                                return androidx.compose.ui.geometry.Offset.Zero
                            }
                        }
                    }
                    
                    Box(modifier = Modifier.fillMaxSize().nestedScroll(nestedScrollConnection).horizontalScroll(pageScrollState)) {"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
