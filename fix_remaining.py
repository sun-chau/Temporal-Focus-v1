import re

files_to_fix = [
    'app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt',
    'app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt',
    'app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt',
    'app/src/main/java/com/example/ui/utils/LabelUtils.kt',
    'app/src/main/java/com/example/viewmodel/MainViewModel.kt',
    'app/src/main/java/com/example/data/DailyScheduleDao.kt'
]

for file_path in files_to_fix:
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            
        content = re.sub(r'\btags\b', 'labels', content)
        content = re.sub(r'\btag\b', 'label', content)
        
        # In MainViewModel.kt:
        # e: file:///app/src/main/java/com/example/viewmodel/MainViewModel.kt:277:13 Argument already passed for this parameter.
        # This is `customLabels = appSettings.customLabels` duplicate in init
        if "MainViewModel.kt" in file_path:
            content = re.sub(r'(customLabels = appSettings\.customLabels,\s*)customLabels = appSettings\.customLabels,', r'\1', content)
            
        with open(file_path, 'w') as f:
            f.write(content)
    except FileNotFoundError:
        pass
