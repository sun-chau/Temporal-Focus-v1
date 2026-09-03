import re

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()

# Add the import
if 'import com.google.gson.Gson' not in content:
    content = content.replace('import androidx.lifecycle.viewModelScope', 'import androidx.lifecycle.viewModelScope\nimport com.google.gson.Gson\nimport com.example.data.*')

# Add the gson instance and functions inside the MainViewModel class
gson_logic = """
    private val gson = Gson()

    fun getParsedPayload(entity: TrackerEntity): Any? {
        return try {
            when (entity.type) {
                TrackerType.SYLLABUS -> gson.fromJson(entity.payloadData, SyllabusPayload::class.java) ?: SyllabusPayload()
                TrackerType.ASSIGNMENT -> gson.fromJson(entity.payloadData, AssignmentPayload::class.java) ?: AssignmentPayload()
                else -> null
            }
        } catch (e: Exception) {
            null
        }
    }

    fun updateSyllabusPayload(entity: TrackerEntity, payload: SyllabusPayload) {
        val newData = gson.toJson(payload)
        updateTracker(entity.copy(payloadData = newData, lastModified = System.currentTimeMillis()))
    }

    fun updateAssignmentPayload(entity: TrackerEntity, payload: AssignmentPayload) {
        val newData = gson.toJson(payload)
        updateTracker(entity.copy(payloadData = newData, lastModified = System.currentTimeMillis()))
    }
"""

if 'private val gson = Gson()' not in content:
    content = content.replace('fun insertTracker', gson_logic + '\n    fun insertTracker')

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
    f.write(content)
