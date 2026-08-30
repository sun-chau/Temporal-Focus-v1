import re

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()

# Fix UiState duplicates
content = re.sub(r'val customLabels: Set<String> = [^\n]*\n\s*val customLabels: Set<String> = [^\n]*\n', r'val customLabels: Set<String> = setOf("Work", "Study", "Personal", "Health", "Leisure", "Other"),\n', content)
content = re.sub(r'val coloredLabelsEnabled: Boolean = [^\n]*\n\s*val coloredLabelsEnabled: Boolean = [^\n]*\n', r'val coloredLabelsEnabled: Boolean = true,\n', content)

# Fix init duplicates
content = re.sub(r'customLabels = appSettings\.customLabels,\s*customLabels = appSettings\.customLabels,', r'customLabels = appSettings.customLabels,', content)
content = re.sub(r'coloredLabelsEnabled = appSettings\.coloredLabelsEnabled,\s*coloredLabelsEnabled = appSettings\.coloredLabelsEnabled,', r'coloredLabelsEnabled = appSettings.coloredLabelsEnabled,', content)

# Remove duplicate addCustomLabel
pattern_add = r'    fun addCustomLabel\(.*?\)\s*\{[\s\S]*?\}'
matches = list(re.finditer(pattern_add, content))
if len(matches) > 1:
    content = content[:matches[1].start()] + content[matches[1].end():]

# Remove duplicate removeCustomLabel
pattern_remove = r'    fun removeCustomLabel\(.*?\)\s*\{[\s\S]*?\}'
matches = list(re.finditer(pattern_remove, content))
if len(matches) > 1:
    content = content[:matches[1].start()] + content[matches[1].end():]

# Remove duplicate toggleColoredLabelsEnabled
pattern_toggle = r'    fun toggleColoredLabelsEnabled\(.*?\)\s*\{[\s\S]*?\}'
matches = list(re.finditer(pattern_toggle, content))
if len(matches) > 1:
    content = content[:matches[1].start()] + content[matches[1].end():]

# Fix profile reset
content = content.replace('customLabels = emptySet(), customLabels = emptySet()', 'customLabels = emptySet()')
content = content.replace('appSettings.customLabels = emptySet()\n        appSettings.customLabels = emptySet()', 'appSettings.customLabels = emptySet()')

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
    f.write(content)
