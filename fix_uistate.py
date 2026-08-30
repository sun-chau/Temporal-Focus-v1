import re

path = 'app/src/main/java/com/example/viewmodel/MainViewModel.kt'
with open(path, 'r') as f:
    content = f.read()

content = content.replace(
    """    val currentTheme: String = "Midnight Minimalist",""",
    """    val currentTheme: String = "Midnight Minimalist",
    val customBackdropColor: String = "",
    val customBaseTextColor: String = "",
    val customOverdueTextColor: String = ","""
)

with open(path, 'w') as f:
    f.write(content)
