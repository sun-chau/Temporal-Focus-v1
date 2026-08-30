path = 'app/src/main/java/com/example/viewmodel/MainViewModel.kt'
with open(path, 'r') as f:
    content = f.read()

new_functions = """
    // Settings toggles
    fun togglePreventHidingAllUnits(enabled: Boolean) {
        appSettings.preventHidingAllUnits = enabled
        _uiState.update { it.copy(preventHidingAllUnits = enabled) }
    }
    
    fun togglePomodoroPhaseAlerts(enabled: Boolean) {
        appSettings.pomodoroPhaseAlerts = enabled
        _uiState.update { it.copy(pomodoroPhaseAlerts = enabled) }
    }
    
    fun toggleChronometerDeadlinesAlerts(enabled: Boolean) {
        appSettings.chronometerDeadlinesAlerts = enabled
        _uiState.update { it.copy(chronometerDeadlinesAlerts = enabled) }
    }
    
    fun toggleAlertSound(enabled: Boolean) {
        appSettings.alertSoundEnabled = enabled
        _uiState.update { it.copy(alertSoundEnabled = enabled) }
    }
    
    fun toggleAlertVibration(enabled: Boolean) {
        appSettings.alertVibrationEnabled = enabled
        _uiState.update { it.copy(alertVibrationEnabled = enabled) }
    }
    
    fun toggleAppPasswordEnabled(enabled: Boolean) {
        appSettings.appPasswordEnabled = enabled
        _uiState.update { it.copy(appPasswordEnabled = enabled) }
    }
    
    fun setAppPassword(password: String) {
        appSettings.appPassword = password
        _uiState.update { it.copy(appPassword = password) }
    }
    
    fun toggleBiometricsEnabled(enabled: Boolean) {
        appSettings.biometricsEnabled = enabled
        _uiState.update { it.copy(biometricsEnabled = enabled) }
    }
    
    fun setAuthenticated(auth: Boolean) {
        _uiState.update { it.copy(isAuthenticated = auth) }
    }
    
    fun clearHistory() {
        viewModelScope.launch {
            repository.deleteAllCompletedTasks()
        }
    }
}"""

import re
# Append to end of class (replace last '}' with new_functions)
content = re.sub(r'}\s*$', new_functions, content)

with open(path, 'w') as f:
    f.write(content)
