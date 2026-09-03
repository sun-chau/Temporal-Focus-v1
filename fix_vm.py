import re
with open("app/src/main/java/com/example/viewmodel/TrackerViewModel.kt", "r") as f:
    content = f.read()

new_methods = """
    // Custom Tracker Mutations
    fun deleteCustomEntry(tracker: TrackerEntity, entryId: String) {
        val payload = getParsedPayload(tracker) as? CustomPayload ?: return
        val newEntries = payload.entries.filter { it.id != entryId }
        updateCustomPayload(tracker, payload.copy(entries = newEntries))
    }

    fun updateCustomEntry(tracker: TrackerEntity, entryId: String, newFieldData: Map<String, String>) {
        val payload = getParsedPayload(tracker) as? CustomPayload ?: return
        val newEntries = payload.entries.map {
            if (it.id == entryId) it.copy(fieldData = newFieldData) else it
        }
        updateCustomPayload(tracker, payload.copy(entries = newEntries))
    }

    fun insertTracker"""

content = content.replace("    fun insertTracker", new_methods)

with open("app/src/main/java/com/example/viewmodel/TrackerViewModel.kt", "w") as f:
    f.write(content)
