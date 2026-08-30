import re

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

search_str = '''    fun setMaxStageSlots(slots: Int) {
        appSettings.maxStageSlots = slots
        val currentIds = appSettings.selectedDisplayIds.split(",").filter { it.isNotEmpty() }.toMutableList()
        var updatedIds = currentIds
        if (currentIds.size > slots) {
            while (currentIds.size > slots) {
                currentIds.removeAt(0)
            }
            appSettings.selectedDisplayIds = currentIds.joinToString(",")
            updatedIds = currentIds
        }'''

replace_str = '''    fun setMaxStageSlots(slots: Int) {
        appSettings.maxStageSlots = slots
        val currentIds = appSettings.selectedDisplayIds.split(",").filter { it.isNotEmpty() }.toMutableList()
        var updatedIds = currentIds
        if (slots != -1 && currentIds.size > slots) {
            while (currentIds.size > slots) {
                currentIds.removeAt(0)
            }
            appSettings.selectedDisplayIds = currentIds.joinToString(",")
            updatedIds = currentIds
        }'''

content = content.replace(search_str, replace_str)

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
