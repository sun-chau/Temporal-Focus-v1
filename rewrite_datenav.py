import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Add LaunchedEffect import if needed
if "import androidx.compose.runtime.LaunchedEffect" not in content:
    content = content.replace("import androidx.compose.runtime.*", "import androidx.compose.runtime.*\nimport androidx.compose.runtime.LaunchedEffect")
if "import kotlinx.coroutines.launch" not in content:
    content = content.replace("import androidx.compose.runtime.*", "import androidx.compose.runtime.*\nimport kotlinx.coroutines.launch")

# We want to replace the whole DateNavigator function to implement center scrolling.
search_func = re.compile(r'@Composable\s*fun DateNavigator\(selectedDateMillis: Long, onDateSelected: \(Long\) -> Unit\) \{[\s\S]*?\}\s*(?=@Composable|$)')

replacement = '''@Composable
fun DateNavigator(selectedDateMillis: Long, onDateSelected: (Long) -> Unit) {
    val dates = remember {
        val list = mutableListOf<Long>()
        val today = getStartOfDayMillis(System.currentTimeMillis())
        for (i in -14..14) {
            list.add(today + i * 24 * 60 * 60 * 1000L)
        }
        list
    }
    
    val listState = rememberLazyListState()
    val scope = rememberCoroutineScope()
    
    // Scroll to center when selectedDateMillis changes
    LaunchedEffect(selectedDateMillis) {
        val index = dates.indexOfFirst { it == selectedDateMillis }
        if (index != -1) {
            // Approximation to center the item (screen width / item width)
            // We just animate to the index with a slight offset
            listState.animateScrollToItem(maxOf(0, index - 3))
        }
    }
        
    LazyRow(
        state = listState,
        modifier = Modifier.fillMaxWidth(),
        contentPadding = PaddingValues(horizontal = 16.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(dates) { dateMillis ->
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
                java.util.Calendar.JANUARY -> "Jan"
                java.util.Calendar.FEBRUARY -> "Feb"
                java.util.Calendar.MARCH -> "Mar"
                java.util.Calendar.APRIL -> "Apr"
                java.util.Calendar.MAY -> "May"
                java.util.Calendar.JUNE -> "Jun"
                java.util.Calendar.JULY -> "Jul"
                java.util.Calendar.AUGUST -> "Aug"
                java.util.Calendar.SEPTEMBER -> "Sep"
                java.util.Calendar.OCTOBER -> "Oct"
                java.util.Calendar.NOVEMBER -> "Nov"
                java.util.Calendar.DECEMBER -> "Dec"
                else -> ""
            }
            val isSelected = dateMillis == selectedDateMillis
            val isToday = dateMillis == getStartOfDayMillis(System.currentTimeMillis())
            
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
                        onDateSelected(dateMillis)
                        scope.launch {
                            val index = dates.indexOfFirst { it == dateMillis }
                            if (index != -1) {
                                listState.animateScrollToItem(maxOf(0, index - 3))
                            }
                        }
                    }
                    .padding(8.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                Text(
                    text = dayOfWeek,
                    fontSize = 12.sp,
                    color = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f)
                )
                Spacer(modifier = Modifier.height(0.dp))
                Text(
                    text = dayOfMonth,
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold,
                    color = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurface
                )
                Spacer(modifier = Modifier.height(0.dp))
                Text(
                    text = monthStr,
                    fontSize = 12.sp,
                    color = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f)
                )
            }
        }
    }
}
'''

content = search_func.sub(replacement, content)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
