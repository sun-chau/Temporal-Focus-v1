import re

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()

target = "    fun saveAdvancedDailySchedule(draft: com.example.data.DailyScheduleDraft) {"
replacement = "    fun saveAdvancedDailySchedule(draft: com.example.data.DailyScheduleDraft, editEntireSeries: Boolean = false) {"
content = content.replace(target, replacement)

# Now, we need to inject the editEntireSeries logic into saveAdvancedDailySchedule
# Wait, let's just do it directly.
# Inside saveAdvancedDailySchedule, there is a check for `if (draft.editingId != null)`
target2 = """            if (draft.editingId != null) {
                val existing = db.dailyScheduleDao().getScheduleSync(draft.editingId)
                if (existing != null) {
                    db.dailyScheduleDao().deleteSchedule(existing)
                }
            }"""

replacement2 = """            var targetSeriesId = draft.seriesId
            if (draft.editingId != null) {
                val existing = db.dailyScheduleDao().getScheduleSync(draft.editingId)
                if (existing != null) {
                    if (editEntireSeries && existing.seriesId != null) {
                        val timeDelta = draft.startTime - existing.startTime
                        db.dailyScheduleDao().updateSeries(existing.seriesId, draft.title, draft.tag, timeDelta)
                        recalculateAllLanes(db)
                        clearDailyScheduleDraft()
                        return@launch
                    } else {
                        if (targetSeriesId != null) {
                            db.dailyScheduleDao().breakFromSeries(draft.editingId)
                            targetSeriesId = null
                        }
                        db.dailyScheduleDao().deleteSchedule(existing)
                    }
                }
            }"""

content = content.replace(target2, replacement2)

# Insert seriesId and recurrenceType to insertSchedule
target3 = """                        id = draft.editingId ?: java.util.UUID.randomUUID().toString(),
                        title = draft.title,
                        startTime = draft.startTime,
                        endTime = draft.endTime,
                        tag = draft.tag
                    )"""

replacement3 = """                        id = draft.editingId ?: java.util.UUID.randomUUID().toString(),
                        title = draft.title,
                        startTime = draft.startTime,
                        endTime = draft.endTime,
                        tag = draft.tag,
                        seriesId = targetSeriesId
                    )"""

content = content.replace(target3, replacement3)

# Then in the loop:
target4 = """                while (occurrences < limit && iterations < 3650) {"""
replacement4 = """                if (targetSeriesId == null) { targetSeriesId = java.util.UUID.randomUUID().toString() }
                val maxDays = appSettings.recurrenceGenerationCapYears * 365
                while (occurrences < limit && iterations < maxDays) {"""

content = content.replace(target4, replacement4)

# And inside the loop insertSchedule:
target5 = """                        val taskId = if (occurrences == 0 && draft.editingId != null) draft.editingId else java.util.UUID.randomUUID().toString()
                        db.dailyScheduleDao().insertSchedule(
                            com.example.data.DailyScheduleTask(
                                id = taskId,
                                title = draft.title,
                                startTime = currentStart,
                                endTime = currentEnd,
                                tag = draft.tag
                            )
                        )"""

replacement5 = """                        val taskId = if (occurrences == 0 && draft.editingId != null) draft.editingId else java.util.UUID.randomUUID().toString()
                        db.dailyScheduleDao().insertSchedule(
                            com.example.data.DailyScheduleTask(
                                id = taskId,
                                title = draft.title,
                                startTime = currentStart,
                                endTime = currentEnd,
                                tag = draft.tag,
                                seriesId = targetSeriesId,
                                recurrenceType = draft.recurrenceType.name
                            )
                        )"""
content = content.replace(target5, replacement5)

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
    f.write(content)
