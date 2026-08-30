import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Add onReschedule to ScheduleBlock signature
target_sig = """    blockWidth: androidx.compose.ui.unit.Dp,
    onClick: () -> Unit,
    onStatusChange: (ScheduleStatus) -> Unit
) {"""
replacement_sig = """    blockWidth: androidx.compose.ui.unit.Dp,
    onClick: () -> Unit,
    onStatusChange: (ScheduleStatus) -> Unit,
    onReschedule: () -> Unit
) {"""
content = content.replace(target_sig, replacement_sig)

# Add Reschedule to Dropdown Menu
target_dropdown = """                                onStatusChange(statusOption)
                                showStatusMenu = false
                            }
                        )
                    }
                }
            }
        }
    }
}"""
replacement_dropdown = """                                onStatusChange(statusOption)
                                showStatusMenu = false
                            }
                        )
                    }
                    androidx.compose.material3.HorizontalDivider()
                    DropdownMenuItem(
                        text = { Text("Reschedule") },
                        onClick = {
                            onReschedule()
                            showStatusMenu = false
                        }
                    )
                }
            }
        }
    }
}"""
content = content.replace(target_dropdown, replacement_dropdown)

# Add onReschedule to ScheduleBlock call
target_call = """                                onStatusChange = { newStatus ->
                                    viewModel.updateDailySchedule(schedule.copy(status = newStatus.name, isFinished = (newStatus == ScheduleStatus.COMPLETED || newStatus == ScheduleStatus.SKIPPED || newStatus == ScheduleStatus.DROPPED)))
                                }
                            )
                        }"""
replacement_call = """                                onStatusChange = { newStatus ->
                                    viewModel.updateDailySchedule(schedule.copy(status = newStatus.name, isFinished = (newStatus == ScheduleStatus.COMPLETED || newStatus == ScheduleStatus.SKIPPED || newStatus == ScheduleStatus.DROPPED)))
                                },
                                onReschedule = {
                                    reschedulingSchedule = schedule
                                }
                            )
                        }"""
content = content.replace(target_call, replacement_call)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
print("Reschedule applied successfully")
