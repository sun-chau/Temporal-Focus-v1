import re

with open('app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt', 'r') as f:
    content = f.read()

target = """                                    viewModel.updateDailyScheduleDraft(
                                        com.example.data.DailyScheduleDraft(
                                            title = schedule.title,
                                            startTime = schedule.startTime,
                                            endTime = schedule.endTime,
                                            tag = schedule.tag,
                                            editingId = schedule.id
                                        )
                                    )"""

replacement = """                                    val recType = try { if (schedule.recurrenceType != null) com.example.data.RecurrenceType.valueOf(schedule.recurrenceType) else com.example.data.RecurrenceType.DAILY } catch(e: Exception) { com.example.data.RecurrenceType.DAILY }
                                    viewModel.updateDailyScheduleDraft(
                                        com.example.data.DailyScheduleDraft(
                                            title = schedule.title,
                                            startTime = schedule.startTime,
                                            endTime = schedule.endTime,
                                            tag = schedule.tag,
                                            editingId = schedule.id,
                                            seriesId = schedule.seriesId,
                                            isRecurring = schedule.seriesId != null,
                                            recurrenceType = recType
                                        )
                                    )"""

new_content = content.replace(target, replacement)
with open('app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt', 'w') as f:
    f.write(new_content)
