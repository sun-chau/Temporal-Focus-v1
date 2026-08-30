import re

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

old_func = """fun clearDailyScheduleDraft() {
        _uiState.update { it.copy(dailyScheduleDraft = com.example.data.DailyScheduleDraft(tag = it.customCategories.firstOrNull() ?: "Work")) }
    }"""
new_func = """fun clearDailyScheduleDraft() {
        _uiState.update { it.copy(dailyScheduleDraft = com.example.data.DailyScheduleDraft(tag = "")) }
    }"""
content = content.replace(old_func, new_func)

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt", "r") as f:
    content2 = f.read()

old_click = ".clickable { selectedTag = tag }"
new_click = ".clickable { selectedTag = if (selectedTag == tag) \"\" else tag }"
content2 = content2.replace(old_click, new_click)

with open("app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt", "w") as f:
    f.write(content2)

with open("app/src/main/java/com/example/ui/utils/TagUtils.kt", "r") as f:
    content3 = f.read()

old_getTagColor = "if (!isEnabled) return Color.Transparent"
new_getTagColor = "if (!isEnabled || tag.isBlank()) return Color.Transparent"
content3 = content3.replace(old_getTagColor, new_getTagColor)

with open("app/src/main/java/com/example/ui/utils/TagUtils.kt", "w") as f:
    f.write(content3)
