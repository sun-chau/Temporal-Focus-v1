import re
with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

content = content.replace("com.example.R.mipmap.ic_launcher_orange", "com.example.R.drawable.ic_launcher_foreground_orange")
content = content.replace("com.example.R.mipmap.ic_launcher_obsidian", "com.example.R.drawable.ic_launcher_foreground_obsidian")
content = content.replace("com.example.R.mipmap.ic_launcher_daylight", "com.example.R.drawable.ic_launcher_foreground_daylight")
content = content.replace("com.example.R.mipmap.ic_launcher_midnight", "com.example.R.drawable.ic_launcher_foreground_midnight")
content = content.replace("com.example.R.mipmap.ic_launcher_nordic", "com.example.R.drawable.ic_launcher_foreground_nordic")
content = content.replace("com.example.R.mipmap.ic_launcher_forest", "com.example.R.drawable.ic_launcher_foreground_forest")
content = content.replace("com.example.R.mipmap.ic_launcher_crimson", "com.example.R.drawable.ic_launcher_foreground_crimson")
content = content.replace("com.example.R.mipmap.ic_launcher_amber", "com.example.R.drawable.ic_launcher_foreground_amber")
content = content.replace("com.example.R.mipmap.ic_launcher_monochrome", "com.example.R.drawable.ic_launcher_foreground_monochrome")

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)
