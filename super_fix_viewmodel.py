import re

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()

# Fix duplicates in UiState
lines = content.split('\n')
new_lines = []
seen_custom_labels = False
seen_colored_labels = False
in_ui_state = False

for i, line in enumerate(lines):
    if 'data class UiState(' in line:
        in_ui_state = True
    
    if in_ui_state and line.strip().startswith('val customLabels:'):
        if seen_custom_labels:
            continue
        seen_custom_labels = True
        new_lines.append('    val customLabels: Set<String> = setOf("Work", "Study", "Personal", "Health", "Leisure", "Other"),')
        continue
        
    if in_ui_state and line.strip().startswith('val coloredLabelsEnabled:'):
        if seen_colored_labels:
            continue
        seen_colored_labels = True
        new_lines.append('    val coloredLabelsEnabled: Boolean = true,')
        continue
        
    if in_ui_state and line.strip().startswith('// --- Actions ---'):
        in_ui_state = False

    new_lines.append(line)

content = '\n'.join(new_lines)

# Remove the stray closing braces at line ~962
stray_braces = """    fun removeCustomLabel(category: String) {
        val currentCategories = appSettings.customLabels.toMutableSet()
        if (currentCategories.remove(category)) {
            appSettings.customLabels = currentCategories
            _uiState.update { it.copy(customLabels = currentCategories) }
        }
    }
        }
    }
        }
    }"""

fixed_braces = """    fun removeCustomLabel(label: String) {
        val currentLabels = appSettings.customLabels.toMutableSet()
        if (currentLabels.remove(label)) {
            appSettings.customLabels = currentLabels
            _uiState.update { it.copy(customLabels = currentLabels) }
        }
    }"""

content = content.replace(stray_braces, fixed_braces)
content = content.replace("fun addCustomLabel(category: String)", "fun addCustomLabel(label: String)")
content = content.replace("category.split", "label.split")
content = content.replace("currentCategories.add(category)", "currentLabels.add(label)")
content = content.replace("val currentCategories", "val currentLabels")
content = content.replace("currentCategories", "currentLabels")

# Fix toggle Colored Labels
toggle_colored = """    fun toggleColoredTagsEnabled(enabled: Boolean) {
        appSettings.coloredLabelsEnabled = enabled
        _uiState.update { it.copy(coloredLabelsEnabled = enabled) }
    }
    fun toggleColoredCategoriesEnabled(enabled: Boolean) {
        appSettings.coloredLabelsEnabled = enabled
        _uiState.update { it.copy(coloredLabelsEnabled = enabled) }
    }"""
    
toggle_colored_fixed = """    fun toggleColoredLabelsEnabled(enabled: Boolean) {
        appSettings.coloredLabelsEnabled = enabled
        _uiState.update { it.copy(coloredLabelsEnabled = enabled) }
    }"""

content = content.replace(toggle_colored, toggle_colored_fixed)

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
    f.write(content)

