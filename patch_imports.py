import re

with open("app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt", "r") as f:
    content = f.read()

imports = """
import com.example.ui.screens.getDayOfWeekName
import com.example.ui.screens.getWeekName
import com.example.ui.screens.getMonthName
import com.example.ui.screens.parseDateString
"""

content = content.replace("import com.example.data.RecurrenceType", "import com.example.data.RecurrenceType" + imports)

with open("app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt", "w") as f:
    f.write(content)
