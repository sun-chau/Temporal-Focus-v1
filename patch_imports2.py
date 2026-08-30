import re

with open("app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt", "r") as f:
    content = f.read()

more_imports = """
import java.util.Calendar
import com.example.data.MonthlyType
import com.example.data.AnnuallyType
"""

content = content.replace("import com.example.data.RecurrenceType", "import com.example.data.RecurrenceType\n" + more_imports)

with open("app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt", "w") as f:
    f.write(content)
