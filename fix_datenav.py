import re
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Replace DateNavigator call
# The original call was:
#            // Header: Date Navigator
#            DateNavigator(selectedDateMillis) { newDate ->
#                selectedDateMillis = newDate
#            }
content = re.sub(
    r"// Header: Date Navigator\n\s*DateNavigator\(selectedDateMillis\) \{ newDate ->\n\s*selectedDateMillis = newDate\n\s*\}",
    "// Header: Date Navigator\n            DateNavigator(pagerState, todayMillis, coroutineScope)",
    content
)

# Replace DateNavigator function definition
datenav_new = """@OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class)
@Composable
fun DateNavigator(pagerState: PagerState, todayMillis: Long, coroutineScope: kotlinx.coroutines.CoroutineScope) {
    val listState = rememberLazyListState()
    
    // Scroll to center when pagerState.currentPage changes
    LaunchedEffect(pagerState.currentPage) {
        val index = pagerState.currentPage - (Int.MAX_VALUE / 2) + 14
        if (index >= 0) {
            listState.animateScrollToItem(maxOf(0, index - 3))
        }
    }
    
    LazyRow(
        state = listState,
        modifier = Modifier.fillMaxWidth(),
        contentPadding = PaddingValues(horizontal = 16.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        // Just generate a window of -14 to +14 days around the current page
        // Wait, if it's infinite, why restrict to 14? We can just use an infinite LazyRow or a large range.
        // For simplicity, let's just make it a large range or centered around the current page.
        // Actually, let's use a large range like 1000 days.
        val startOffset = -500
        val totalItems = 1000
        
        items(totalItems) { index ->
            val dayOffset = startOffset + index
            val dateMillis = todayMillis + dayOffset * 24 * 60 * 60 * 1000L
            val cal = Calendar.getInstance().apply { timeInMillis = dateMillis }
            val dayOfWeek = when (cal.get(Calendar.DAY_OF_WEEK)) {
                Calendar.SUNDAY -> "Sun"
                Calendar.MONDAY -> "Mon"
                Calendar.TUESDAY -> "Tue"
                Calendar.WEDNESDAY -> "Wed"
                Calendar.THURSDAY -> "Thu"
                Calendar.FRIDAY -> "Fri"
                Calendar.SATURDAY -> "Sat"
                else -> ""
            }
            val dayOfMonth = cal.get(Calendar.DAY_OF_MONTH).toString()
            val monthStr = when (cal.get(Calendar.MONTH)) {
                Calendar.JANUARY -> "Jan"
                Calendar.FEBRUARY -> "Feb"
                Calendar.MARCH -> "Mar"
                Calendar.APRIL -> "Apr"
                Calendar.MAY -> "May"
                Calendar.JUNE -> "Jun"
                Calendar.JULY -> "Jul"
                Calendar.AUGUST -> "Aug"
                Calendar.SEPTEMBER -> "Sep"
                Calendar.OCTOBER -> "Oct"
                Calendar.NOVEMBER -> "Nov"
                Calendar.DECEMBER -> "Dec"
                else -> ""
            }
            
            val absolutePage = (Int.MAX_VALUE / 2) + dayOffset
            val isSelected = pagerState.currentPage == absolutePage
            val isToday = dayOffset == 0
            
            Column(
                modifier = Modifier
                    .width(56.dp)
                    .height(84.dp)
                    .clip(RoundedCornerShape(32.dp))
                    .background(
                        if (isSelected) MaterialTheme.colorScheme.primary 
                        else MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
                    )
                    .border(
                        if (isToday && !isSelected) BorderStroke(1.dp, MaterialTheme.colorScheme.primary) 
                        else BorderStroke(0.dp, Color.Transparent),
                        RoundedCornerShape(32.dp)
                    )
                    .clickable { 
                        coroutineScope.launch {
                            pagerState.animateScrollToPage(absolutePage)
                        }
                    },
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                Text(
                    text = monthStr,
                    style = MaterialTheme.typography.labelSmall,
                    color = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text(
                    text = dayOfMonth,
                    style = MaterialTheme.typography.titleLarge.copy(fontWeight = FontWeight.Bold),
                    color = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text(
                    text = dayOfWeek,
                    style = MaterialTheme.typography.labelSmall,
                    color = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    }
}
"""

content = re.sub(
    r"fun DateNavigator\(selectedDateMillis: Long, onDateSelected: \(Long\) -> Unit\) \{.*?\n\}\n",
    datenav_new + "\n",
    content,
    flags=re.DOTALL
)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
