import re

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "r") as f:
    content = f.read()

search_str1 = r'''"Urgency Engine Override Active: The application is dynamically displaying the \$\{uiState\.maxStageSlots\} nearest target deadlines\.",'''
replace_str1 = '''"Urgency Engine Override Active: The application is dynamically displaying the ${if (uiState.maxStageSlots == -1) "all" else uiState.maxStageSlots} nearest target deadlines.",'''

content = re.sub(search_str1, replace_str1, content)

search_str2 = r'''"Custom Manual Pinning Active: Select up to \$\{uiState\.maxStageSlots\} timers from the list below to pin them onto your main Stage\.",'''
replace_str2 = '''"Custom Manual Pinning Active: Select up to ${if (uiState.maxStageSlots == -1) "unlimited" else uiState.maxStageSlots} timers from the list below to pin them onto your main Stage.",'''

content = re.sub(search_str2, replace_str2, content)

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "w") as f:
    f.write(content)
