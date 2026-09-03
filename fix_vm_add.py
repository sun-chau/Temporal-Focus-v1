import re
with open("app/src/main/java/com/example/viewmodel/TrackerViewModel.kt", "r") as f:
    content = f.read()

new_methods = """
    fun addCustomEntry(tracker: TrackerEntity, fieldData: Map<String, String>) {
        val payload = getParsedPayload(tracker) as? CustomPayload ?: return
        val newEntry = CustomEntry(
            timestampEpoch = System.currentTimeMillis(),
            fieldData = fieldData
        )
        updateCustomPayload(tracker, payload.copy(entries = payload.entries + newEntry))
    }

    fun insertTracker"""

content = content.replace("    fun insertTracker", new_methods)

with open("app/src/main/java/com/example/viewmodel/TrackerViewModel.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/screens/CustomTrackerUI.kt", "r") as f:
    ui_content = f.read()

ui_content = ui_content.replace(
"""                    val newEntry = CustomEntry(
                        timestampEpoch = System.currentTimeMillis(),
                        fieldData = inputValues
                    )
                    viewModel.updateCustomPayload(entity, payload.copy(entries = payload.entries + newEntry))""",
"                    viewModel.addCustomEntry(entity, inputValues)"
)

with open("app/src/main/java/com/example/ui/screens/CustomTrackerUI.kt", "w") as f:
    f.write(ui_content)
