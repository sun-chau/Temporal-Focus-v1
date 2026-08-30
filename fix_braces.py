import re

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()

# Replace the specific block
pattern = r'    fun removeCustomLabel\([^\)]*\)\s*\{\s*val [^\n]*\s*if \([^\)]*\)\s*\{\s*appSettings[^\n]*\n\s*_uiState[^\n]*\n\s*\}\s*\}\s*\}\s*\}\s*\}\s*\}'
import re
# Actually simpler:
old_part = """    fun removeCustomLabel(category: String) {
        val currentLabels = appSettings.customLabels.toMutableSet()
        if (currentLabels.remove(category)) {
            appSettings.customLabels = currentLabels
            _uiState.update { it.copy(customLabels = currentLabels) }
        }
    }
        }
    }
        }
    }"""
new_part = """    fun removeCustomLabel(label: String) {
        val currentLabels = appSettings.customLabels.toMutableSet()
        if (currentLabels.remove(label)) {
            appSettings.customLabels = currentLabels
            _uiState.update { it.copy(customLabels = currentLabels) }
        }
    }"""

content = content.replace(old_part, new_part)

# Also fix the toggle duplicate functions
old_toggle = """    fun toggleColoredTagsEnabled(enabled: Boolean) {
        appSettings.coloredLabelsEnabled = enabled
        _uiState.update { it.copy(coloredLabelsEnabled = enabled) }
    }
    fun toggleColoredCategoriesEnabled(enabled: Boolean) {
        appSettings.coloredLabelsEnabled = enabled
        _uiState.update { it.copy(coloredLabelsEnabled = enabled) }
    }"""
new_toggle = """    fun toggleColoredLabelsEnabled(enabled: Boolean) {
        appSettings.coloredLabelsEnabled = enabled
        _uiState.update { it.copy(coloredLabelsEnabled = enabled) }
    }"""
content = content.replace(old_toggle, new_toggle)

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
    f.write(content)

