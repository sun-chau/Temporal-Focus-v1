import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

target = "Box(modifier = Modifier.fillMaxSize().horizontalScroll(pageScrollState)) {"

replacement = """
                    val nestedScrollConnection = remember(pageScrollState) {
                        object : androidx.compose.ui.input.nestedscroll.NestedScrollConnection {
                            override fun onPreScroll(available: androidx.compose.ui.geometry.Offset, source: androidx.compose.ui.input.nestedscroll.NestedScrollSource): androidx.compose.ui.geometry.Offset {
                                val canScrollForward = pageScrollState.value < pageScrollState.maxValue
                                val canScrollBackward = pageScrollState.value > 0
                                
                                val tryingToPanBackward = available.x > 0
                                val tryingToPanForward = available.x < 0
                                
                                // If we are at the edge and trying to pan past it, we let the parent (Pager) consume it.
                                // Actually, returning Offset.Zero means we DON'T consume it, letting the child evaluate.
                                // But horizontalScroll might consume it if not careful.
                                // Wait, returning Offset.Zero is the default anyway.
                                // To force the pager to take it, maybe we don't need to do anything special here if horizontalScroll works.
                                return androidx.compose.ui.geometry.Offset.Zero
                            }
                        }
                    }
                    Box(modifier = Modifier.fillMaxSize().nestedScroll(nestedScrollConnection).horizontalScroll(pageScrollState)) {"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
