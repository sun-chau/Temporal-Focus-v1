with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()

content = content.replace("            customColors = appSettings.customColors,\n            customLabels = appSettings.customLabels,", "            customColors = appSettings.customColors,")

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
    f.write(content)
