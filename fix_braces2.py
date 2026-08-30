import re

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()

pattern = r'(    fun removeCustomLabel\([^\)]*\)\s*\{\s*val [^\n]*\s*if \([^\)]*\)\s*\{\s*appSettings[^\n]*\n\s*_uiState[^\n]*\n\s*\}\s*\})([\s\}]+)(    fun deleteAccount\(\))'

def repl(m):
    return m.group(1) + '\n\n' + m.group(3)

content = re.sub(pattern, repl, content)

# Change the category parameter to label
content = content.replace("fun removeCustomLabel(category: String)", "fun removeCustomLabel(label: String)")

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
    f.write(content)
