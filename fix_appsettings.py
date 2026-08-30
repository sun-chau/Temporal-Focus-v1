import re

with open('app/src/main/java/com/example/data/AppSettings.kt', 'r') as f:
    content = f.read()

# Fix duplicates in AppSettings
# It has two var customLabels, two var coloredLabelsEnabled

pattern_custom_labels = r'    var customLabels: Set<String>[\s\S]*?apply\(\)'
matches = list(re.finditer(pattern_custom_labels, content))
if len(matches) == 2:
    # Remove the second one
    content = content[:matches[1].start()] + content[matches[1].end():]
    
pattern_colored_labels = r'    var coloredLabelsEnabled: Boolean[\s\S]*?apply\(\)'
matches = list(re.finditer(pattern_colored_labels, content))
if len(matches) == 2:
    # Remove the second one
    content = content[:matches[1].start()] + content[matches[1].end():]

# Ensure default labels includes categories
content = content.replace('setOf("Work", "Personal", "Health", "Study")', 'setOf("Work", "Personal", "Health", "Study", "Leisure", "Other")')

with open('app/src/main/java/com/example/data/AppSettings.kt', 'w') as f:
    f.write(content)
