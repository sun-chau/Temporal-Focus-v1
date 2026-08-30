import re

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'r') as f:
    content = f.read()

old_logic = """                                            if (!uiState.isPomodoroRunning && !uiState.hasPomodoroStarted) {
                                                when (uiState.currentPhase) {
                                                    PomodoroPhase.FOCUS -> viewModel.adjustBaseFocusTime(minutesDelta)
                                                    PomodoroPhase.BREAK -> viewModel.adjustBaseBreakTime(minutesDelta)
                                                    PomodoroPhase.LONG_BREAK -> viewModel.adjustLongBreakTime(minutesDelta)
                                                }
                                            } else {
                                                viewModel.addLiveExtraTime((minutesDelta * 60).toLong())
                                            }"""

new_logic = """                                            if (!uiState.hasPomodoroStarted) {
                                                when (uiState.currentPhase) {
                                                    PomodoroPhase.FOCUS -> viewModel.adjustBaseFocusTime(minutesDelta)
                                                    PomodoroPhase.BREAK -> viewModel.adjustBaseBreakTime(minutesDelta)
                                                    PomodoroPhase.LONG_BREAK -> viewModel.adjustLongBreakTime(minutesDelta)
                                                }
                                            }"""

content = content.replace(old_logic, new_logic)

# Also let's wrap the detectVerticalDragGestures so it's not even registered if hasPomodoroStarted
old_pointer_input = """                            .pointerInput(uiState.isPomodoroRunning, uiState.hasPomodoroStarted) {
                                detectVerticalDragGestures("""

new_pointer_input = """                            .pointerInput(uiState.hasPomodoroStarted) {
                                if (!uiState.hasPomodoroStarted) {
                                    detectVerticalDragGestures("""

content = content.replace(old_pointer_input, new_pointer_input)

# And we need to add the closing brace for the if statement. 
# It currently looks like:
#                                         }
#                                     }
#                                 )
#                             },

old_end = """                                        }
                                    }
                                )
                            },"""

new_end = """                                        }
                                    }
                                )
                                }
                            },"""
                            
content = content.replace(old_end, new_end)


with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'w') as f:
    f.write(content)
