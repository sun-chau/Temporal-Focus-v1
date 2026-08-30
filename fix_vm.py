import re

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()

new_func = """
    fun revertLiveExtraTime() {
        _uiState.update { state ->
            val newRemaining = (state.pomodoroTimeRemainingSeconds - state.sessionExtraTimeSeconds).coerceAtLeast(0L)
            state.copy(
                pomodoroTimeRemainingSeconds = newRemaining,
                sessionExtraTimeSeconds = 0L
            )
        }
    }
"""

content = content.replace("    fun addLiveExtraTime(seconds: Long) {", new_func + "\n    fun addLiveExtraTime(seconds: Long) {")

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
    f.write(content)
