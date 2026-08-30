path = 'app/src/main/java/com/example/viewmodel/MainViewModel.kt'
with open(path, 'r') as f:
    content = f.read()

target_units = """    fun toggleUnitVisibility(unit: String) {
        _uiState.update { state ->
            val newState = when (unit) {
                "Years" -> { appSettings.showYears = !state.showYears; state.copy(showYears = !state.showYears) }
                "Months" -> { appSettings.showMonths = !state.showMonths; state.copy(showMonths = !state.showMonths) }
                "Days" -> { appSettings.showDays = !state.showDays; state.copy(showDays = !state.showDays) }
                "Hours" -> { appSettings.showHours = !state.showHours; state.copy(showHours = !state.showHours) }
                "Minutes" -> { appSettings.showMinutes = !state.showMinutes; state.copy(showMinutes = !state.showMinutes) }
                "Seconds" -> { appSettings.showSeconds = !state.showSeconds; state.copy(showSeconds = !state.showSeconds) }
                else -> state
            }
            newState
        }
    }"""

replacement_units = """    fun toggleUnitVisibility(unit: String) {
        _uiState.update { state ->
            // Prevent hiding all units
            if (state.preventHidingAllUnits) {
                val willTurnOff = when (unit) {
                    "Years" -> state.showYears
                    "Months" -> state.showMonths
                    "Days" -> state.showDays
                    "Hours" -> state.showHours
                    "Minutes" -> state.showMinutes
                    "Seconds" -> state.showSeconds
                    else -> false
                }
                if (willTurnOff) {
                    val activeCount = listOf(state.showYears, state.showMonths, state.showDays, state.showHours, state.showMinutes, state.showSeconds).count { it }
                    if (activeCount <= 1) return@update state // Prevent turning off the last one
                }
            }
            
            val newState = when (unit) {
                "Years" -> { appSettings.showYears = !state.showYears; state.copy(showYears = !state.showYears) }
                "Months" -> { appSettings.showMonths = !state.showMonths; state.copy(showMonths = !state.showMonths) }
                "Days" -> { appSettings.showDays = !state.showDays; state.copy(showDays = !state.showDays) }
                "Hours" -> { appSettings.showHours = !state.showHours; state.copy(showHours = !state.showHours) }
                "Minutes" -> { appSettings.showMinutes = !state.showMinutes; state.copy(showMinutes = !state.showMinutes) }
                "Seconds" -> { appSettings.showSeconds = !state.showSeconds; state.copy(showSeconds = !state.showSeconds) }
                else -> state
            }
            newState
        }
    }"""

content = content.replace(target_units, replacement_units)

with open(path, 'w') as f:
    f.write(content)
