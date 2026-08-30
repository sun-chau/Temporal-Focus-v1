import re

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()

# Replace the stray braces block
pattern_braces = r'(\s*fun removeCustomLabel[^\n]+\n\s*val currentLabels[^\n]+\n\s*if [^\n]+\n\s*appSettings\.customLabels[^\n]+\n\s*_uiState\.update[^\n]+\n\s*\}\n\s*\})(\s*\}){4}'
match = re.search(pattern_braces, content)
if match:
    content = content[:match.start(2)] + content[match.end(2):]
else:
    print("Could not find pattern for braces!")

# Replace toggle colored labels duplication
pattern_toggle = r'    fun toggleColoredTagsEnabled\(enabled: Boolean\) \{\s*appSettings\.coloredLabelsEnabled = enabled\s*_uiState\.update \{ it\.copy\(coloredLabelsEnabled = enabled\) \}\s*\}\s*fun toggleColoredCategoriesEnabled\(enabled: Boolean\) \{\s*appSettings\.coloredLabelsEnabled = enabled\s*_uiState\.update \{ it\.copy\(coloredLabelsEnabled = enabled\) \}\s*\}'
replacement = """    fun toggleColoredLabelsEnabled(enabled: Boolean) {
        appSettings.coloredLabelsEnabled = enabled
        _uiState.update { it.copy(coloredLabelsEnabled = enabled) }
    }"""
content = re.sub(pattern_toggle, replacement, content)

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
    f.write(content)
