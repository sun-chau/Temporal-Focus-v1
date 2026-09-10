import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

target_date = """            val dayOfWeek = when (cal.get(Calendar.DAY_OF_WEEK)) {
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
            
            val absolutePage = (50000) + dayOffset
            val isSelected = pagerState.currentPage == absolutePage
            val isToday = absolutePage == actualTodayPage
            
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
            }"""

replacement_date = """            val dayOfWeek = when (cal.get(Calendar.DAY_OF_WEEK)) {
                Calendar.SUNDAY -> "SUN"
                Calendar.MONDAY -> "MON"
                Calendar.TUESDAY -> "TUE"
                Calendar.WEDNESDAY -> "WED"
                Calendar.THURSDAY -> "THU"
                Calendar.FRIDAY -> "FRI"
                Calendar.SATURDAY -> "SAT"
                else -> ""
            }
            val dayOfMonth = cal.get(Calendar.DAY_OF_MONTH).toString()
            val monthStr = when (cal.get(Calendar.MONTH)) {
                Calendar.JANUARY -> "JAN"
                Calendar.FEBRUARY -> "FEB"
                Calendar.MARCH -> "MAR"
                Calendar.APRIL -> "APR"
                Calendar.MAY -> "MAY"
                Calendar.JUNE -> "JUN"
                Calendar.JULY -> "JUL"
                Calendar.AUGUST -> "AUG"
                Calendar.SEPTEMBER -> "SEP"
                Calendar.OCTOBER -> "OCT"
                Calendar.NOVEMBER -> "NOV"
                Calendar.DECEMBER -> "DEC"
                else -> ""
            }
            
            val absolutePage = (50000) + dayOffset
            val isSelected = pagerState.currentPage == absolutePage
            val isToday = absolutePage == actualTodayPage
            
            val borderStroke = when {
                isToday -> BorderStroke(2.dp, MaterialTheme.colorScheme.outlineVariant)
                !isSelected -> BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
                else -> BorderStroke(0.dp, Color.Transparent)
            }
            
            Column(
                modifier = Modifier
                    .width(56.dp)
                    .height(84.dp)
                    .clip(RectangleShape)
                    .background(
                        if (isSelected) MaterialTheme.colorScheme.primary 
                        else Color.Transparent
                    )
                    .border(
                        borderStroke,
                        RectangleShape
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
                    fontFamily = FontFamily.Monospace,
                    style = MaterialTheme.typography.labelSmall,
                    color = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text(
                    text = dayOfMonth,
                    fontFamily = FontFamily.Monospace,
                    style = MaterialTheme.typography.titleLarge.copy(fontWeight = FontWeight.Bold),
                    color = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text(
                    text = dayOfWeek,
                    fontFamily = FontFamily.Monospace,
                    style = MaterialTheme.typography.labelSmall,
                    color = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                )
            }"""

content = content.replace(target_date, replacement_date)

ruler_target = """        for (hour in 0..24) {
            val offset = (hour * 60 * 2.0).dp
            // Major tick
            Box(
                modifier = Modifier
                    .offset(x = offset)
                    .width(2.dp)
                    .fillMaxHeight()
                    .background(MaterialTheme.colorScheme.onSurface.copy(alpha = 0.3f))
            )
            // Label
            if (hour < 24) {
                Text(
                    text = formatTime(hour, 0, use24HourFormat),
                    fontSize = 10.sp,
                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f),
                    modifier = Modifier
                        .offset(x = offset + 4.dp)
                        .padding(top = 2.dp)
                )
            }
        }"""
        
ruler_replacement = """        for (hour in 0..24) {
            val offset = (hour * 60 * 2.0).dp
            // Major tick
            Box(
                modifier = Modifier
                    .offset(x = offset)
                    .width(1.dp)
                    .fillMaxHeight()
                    .background(MaterialTheme.colorScheme.onSurface.copy(alpha = 0.3f))
            )
            // Label
            if (hour < 24) {
                Text(
                    text = "[ ${formatTime(hour, 0, use24HourFormat)} ]",
                    fontFamily = FontFamily.Monospace,
                    fontSize = 10.sp,
                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f),
                    modifier = Modifier
                        .offset(x = offset + 4.dp)
                        .padding(top = 2.dp)
                )
            }
        }"""

content = content.replace(ruler_target, ruler_replacement)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
print("Date/Ruler Patched")
