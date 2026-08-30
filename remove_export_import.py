import re

with open("app/src/main/java/com/example/ui/screens/MainScreen.kt", "r") as f:
    content = f.read()

# Try to remove Export Data and Import Data items
p_export = re.compile(r'\s*NavigationDrawerItem\(\s*icon = \{ Icon\(Icons\.Outlined\.FileDownload[\s\S]*?Modifier\.padding\(NavigationDrawerItemDefaults\.ItemPadding\)\s*\)')
p_import = re.compile(r'\s*NavigationDrawerItem\(\s*icon = \{ Icon\(Icons\.Outlined\.FileUpload[\s\S]*?Modifier\.padding\(NavigationDrawerItemDefaults\.ItemPadding\)\s*\)')

content = p_export.sub('', content)
content = p_import.sub('', content)

with open("app/src/main/java/com/example/ui/screens/MainScreen.kt", "w") as f:
    f.write(content)
