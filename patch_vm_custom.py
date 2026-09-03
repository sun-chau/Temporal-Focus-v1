import re

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()

# Add CUSTOM to getParsedPayload
content = content.replace(
    'TrackerType.ASSIGNMENT ->',
    'TrackerType.CUSTOM -> gson.fromJson(entity.payloadData, CustomPayload::class.java) ?: CustomPayload()\n                TrackerType.ASSIGNMENT ->'
)

# Add updateCustomPayload
custom_save = """
    fun updateCustomPayload(entity: TrackerEntity, payload: CustomPayload) {
        val newData = gson.toJson(payload)
        updateTracker(entity.copy(payloadData = newData, lastModified = System.currentTimeMillis()))
    }
"""
content = content.replace('fun updateAssignmentPayload', custom_save + '\n    fun updateAssignmentPayload')

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
    f.write(content)
