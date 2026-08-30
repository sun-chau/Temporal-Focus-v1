import re

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

content = content.replace('val currentTheme: String = "Midnight Minimalist",', 'val currentTheme: String = "Monochrome",')

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/theme/Theme.kt", "r") as f:
    content = f.read()

content = content.replace('themeName: String = "Midnight Minimalist",', 'themeName: String = "Monochrome",')

with open("app/src/main/java/com/example/ui/theme/Theme.kt", "w") as f:
    f.write(content)

