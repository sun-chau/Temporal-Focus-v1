with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

old_func = """fun clearDailyScheduleDraft() {
        _uiState.update { it.copy(dailyScheduleDraft = com.example.data.DailyScheduleDraft()) }
    }"""
new_func = """fun clearDailyScheduleDraft() {
        _uiState.update { it.copy(dailyScheduleDraft = com.example.data.DailyScheduleDraft(tag = it.customCategories.firstOrNull() ?: "Work")) }
    }"""

content = content.replace(old_func, new_func)

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
