import re

path = 'app/src/main/java/com/example/viewmodel/MainViewModel.kt'
with open(path, 'r') as f:
    content = f.read()

content = content.replace(
    """            showMinutes = appSettings.showMinutes,
            showSeconds = appSettings.showSeconds,
            currentTheme = appSettings.currentTheme,
            customBackdropColor = appSettings.customBackdropColor,
            customBaseTextColor = appSettings.customBaseTextColor,
            customOverdueTextColor = appSettings.customOverdueTextColor,
            baseFocusDurationMinutes = appSettings.baseFocusDurationMinutes,""",
    """            showMinutes = appSettings.showMinutes,
            showSeconds = appSettings.showSeconds,
            baseFocusDurationMinutes = appSettings.baseFocusDurationMinutes,"""
)

content = content.replace(
    """            currentTheme = appSettings.currentTheme,
            preventHidingAllUnits = appSettings.preventHidingAllUnits,""",
    """            currentTheme = appSettings.currentTheme,
            customBackdropColor = appSettings.customBackdropColor,
            customBaseTextColor = appSettings.customBaseTextColor,
            customOverdueTextColor = appSettings.customOverdueTextColor,
            preventHidingAllUnits = appSettings.preventHidingAllUnits,"""
)

with open(path, 'w') as f:
    f.write(content)
