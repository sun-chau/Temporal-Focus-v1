import re

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()

content = re.sub(r'\s*val showQuickDeadlineSheet: Boolean = false,', '', content)

sheet_setter = """    fun setQuickDeadlineSheet(show: Boolean) {
        _uiState.update { it.copy(showQuickDeadlineSheet = show) }
    }"""
content = content.replace(sheet_setter, "")

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
    f.write(content)
