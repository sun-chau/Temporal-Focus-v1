import os

files_to_fix = [
    'app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt',
    'app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt',
    'app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt',
    'app/src/main/java/com/example/ui/screens/UserAccountScreen.kt',
    'app/src/main/java/com/example/ui/screens/SettingsScreen.kt'
]

for file_path in files_to_fix:
    with open(file_path, 'r') as f:
        content = f.read()
    
    # UserAccountScreen & SettingsScreen
    content = content.replace('toggleColoredTagsEnabled', 'toggleColoredLabelsEnabled')
    content = content.replace('toggleColoredCategoriesEnabled', 'toggleColoredLabelsEnabled')
    content = content.replace('addCustomCategory', 'addCustomLabel')
    content = content.replace('removeCustomCategory', 'removeCustomLabel')
    content = content.replace('tags = ', 'labels = ')
    content = content.replace('tag = ', 'label = ')
    content = content.replace('draft.tags', 'draft.labels')
    content = content.replace('draft.tag', 'draft.label')
    content = content.replace('task.tags', 'task.labels')
    content = content.replace('task.tag', 'task.label')
    
    with open(file_path, 'w') as f:
        f.write(content)
