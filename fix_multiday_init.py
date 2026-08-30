import sys

with open("app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt", "r") as f:
    content = f.read()

old_init = "    var isMultiDay by remember { mutableStateOf(false) }"
new_init = """    var isMultiDay by remember { 
        val startCal = Calendar.getInstance().apply { timeInMillis = draft.startTime }
        val endCal = Calendar.getInstance().apply { timeInMillis = draft.endTime }
        mutableStateOf(
            startCal.get(Calendar.YEAR) != endCal.get(Calendar.YEAR) ||
            startCal.get(Calendar.DAY_OF_YEAR) != endCal.get(Calendar.DAY_OF_YEAR)
        )
    }"""

content = content.replace(old_init, new_init)

with open("app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt", "w") as f:
    f.write(content)
