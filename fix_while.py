with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    lines = f.readlines()

new_lines = lines[:194] + [
"        viewModelScope.launch(Dispatchers.IO) {\n",
"            while (true) {\n",
"                val now = System.currentTimeMillis()\n",
"                val autoStatus = appSettings.autoStatusIfMissed\n",
"                if (autoStatus == \"COMPLETED\" || autoStatus == \"SKIPPED\") {\n",
"                    val schedules = _uiState.value.dailySchedules\n",
"                    for (schedule in schedules) {\n",
"                        if (schedule.endTime < now && schedule.status == \"NOT_DONE\") {\n",
"                            val updated = schedule.copy(status = autoStatus)\n",
"                            database.dailyScheduleDao().updateSchedule(updated)\n",
"                        }\n",
"                    }\n",
"                }\n",
"                kotlinx.coroutines.delay(60000)\n",
"            }\n",
"        }\n",
"        \n",
"        viewModelScope.launch(Dispatchers.IO) {\n",
"            database.dailyScheduleDao().getAllSchedules().collect { schedules ->\n",
"                _uiState.update { it.copy(dailySchedules = schedules) }\n",
"            }\n",
"        }\n"
] + lines[219:]

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.writelines(new_lines)
