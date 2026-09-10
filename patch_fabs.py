import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

target_small_fab = """                    androidx.compose.material3.SmallFloatingActionButton(
                        onClick = { 
                            // We can't scroll to a specific pixel in HorizontalPager directly if it snaps, 
                            // but we can scroll to the page. 
                            coroutineScope.launch {
                                scrollToNowTrigger++
                            }
                        },
                        containerColor = MaterialTheme.colorScheme.primary,
                        contentColor = MaterialTheme.colorScheme.background
                    )"""
replacement_small_fab = """                    androidx.compose.material3.SmallFloatingActionButton(
                        onClick = { 
                            // We can't scroll to a specific pixel in HorizontalPager directly if it snaps, 
                            // but we can scroll to the page. 
                            coroutineScope.launch {
                                scrollToNowTrigger++
                            }
                        },
                        containerColor = MaterialTheme.colorScheme.primary,
                        contentColor = MaterialTheme.colorScheme.background,
                        shape = RectangleShape
                    )"""

content = content.replace(target_small_fab, replacement_small_fab)

target_fab = """                FloatingActionButton(onClick = { 
                    viewModel.clearDailyScheduleDraft()
                    viewModel.setTimerMode(com.example.viewmodel.TimerMode.CREATE_DAILY_SCHEDULE)
                }, containerColor = MaterialTheme.colorScheme.primary, contentColor = MaterialTheme.colorScheme.background) {"""
replacement_fab = """                FloatingActionButton(onClick = { 
                    viewModel.clearDailyScheduleDraft()
                    viewModel.setTimerMode(com.example.viewmodel.TimerMode.CREATE_DAILY_SCHEDULE)
                }, containerColor = MaterialTheme.colorScheme.primary, contentColor = MaterialTheme.colorScheme.background, shape = RectangleShape) {"""

content = content.replace(target_fab, replacement_fab)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
print("FABs Patched")
