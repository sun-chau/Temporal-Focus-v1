with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

datepicker_logic = """
    if (showDatePicker) {
        val currentCal = Calendar.getInstance().apply { timeInMillis = selectedDateMillis }
        DisposableEffect(Unit) {
            val datePickerDialog = DatePickerDialog(
                context,
                { _, year, month, dayOfMonth ->
                    val newCal = Calendar.getInstance().apply {
                        set(year, month, dayOfMonth)
                    }
                    val newMillis = getStartOfDayMillis(newCal.timeInMillis)
                    val daysDiff = ((newMillis - todayMillis) / (24 * 60 * 60 * 1000L)).toInt()
                    val targetPage = (Int.MAX_VALUE / 2) + daysDiff
                    coroutineScope.launch {
                        pagerState.animateScrollToPage(targetPage)
                    }
                    showDatePicker = false
                },
                currentCal.get(Calendar.YEAR),
                currentCal.get(Calendar.MONTH),
                currentCal.get(Calendar.DAY_OF_MONTH)
            )
            datePickerDialog.setOnCancelListener {
                showDatePicker = false
            }
            datePickerDialog.show()
            onDispose {
                datePickerDialog.dismiss()
            }
        }
    }
"""

# Let's insert it right before `if (reschedulingSchedule != null)`
content = content.replace("if (reschedulingSchedule != null) {", datepicker_logic + "\n    if (reschedulingSchedule != null) {")

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
