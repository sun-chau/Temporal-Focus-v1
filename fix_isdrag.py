import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

pattern = r'private fun isDrag\(source: androidx\.compose\.ui\.input\.nestedscroll\.NestedScrollSource\): Boolean \{\s*@Suppress\("DEPRECATION"\)\s*return source == androidx\.compose\.ui\.input\.nestedscroll\.NestedScrollSource\.UserInput \|\| source == androidx\.compose\.ui\.input\.nestedscroll\.NestedScrollSource\.Drag\s*\}'
replacement = """private fun isDrag(source: androidx.compose.ui.input.nestedscroll.NestedScrollSource): Boolean {
                    val s = source.toString()
                    return s.contains("Drag") || s.contains("UserInput")
                }"""

content = re.sub(pattern, replacement, content)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)

print("isDrag reverted")
