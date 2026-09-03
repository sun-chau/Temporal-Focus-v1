import re

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()

# Add GYM to getParsedPayload
content = content.replace(
    'TrackerType.SYLLABUS ->',
    'TrackerType.GYM -> gson.fromJson(entity.payloadData, GymPayload::class.java) ?: GymPayload()\n                TrackerType.SYLLABUS ->'
)

# Add updateGymPayload
gym_save = """
    fun updateGymPayload(entity: TrackerEntity, payload: GymPayload) {
        val newData = gson.toJson(payload)
        updateTracker(entity.copy(payloadData = newData, lastModified = System.currentTimeMillis()))
    }
"""
content = content.replace('fun updateSyllabusPayload', gym_save + '\n    fun updateSyllabusPayload')

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
    f.write(content)
