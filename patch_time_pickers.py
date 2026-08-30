import re

def replace_in_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Replace hardcoded is24Hour in UniversalTimePickerDialog calls
    # Wait, we need to make sure we use uiState.use24HourFormat
    content = re.sub(r'is24Hour\s*=\s*(true|false),', r'is24Hour = uiState.use24HourFormat,', content)

    # For QuickDeadlinesScreen, FAB position
    if "QuickDeadlinesScreen.kt" in filepath:
        content = content.replace('floatingActionButtonPosition = FabPosition.Start', '')

    with open(filepath, 'w') as f:
        f.write(content)

replace_in_file('app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt')
replace_in_file('app/src/main/java/com/example/ui/screens/QuickDeadlinesScreen.kt')
replace_in_file('app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt')
