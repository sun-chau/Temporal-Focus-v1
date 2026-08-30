import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

target_dn_sig = """@Composable
fun DateNavigator(pagerState: PagerState, todayMillis: Long, coroutineScope: kotlinx.coroutines.CoroutineScope) {"""
replacement_dn_sig = """@Composable
fun DateNavigator(pagerState: PagerState, todayMillis: Long, coroutineScope: kotlinx.coroutines.CoroutineScope, actualTodayPage: Int) {"""
content = content.replace(target_dn_sig, replacement_dn_sig)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
