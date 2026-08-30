import re
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

imports = [
    "import androidx.compose.foundation.pager.HorizontalPager",
    "import androidx.compose.foundation.pager.rememberPagerState",
    "import androidx.compose.foundation.pager.PageSize",
    "import androidx.compose.foundation.pager.PagerState"
]

for imp in imports:
    if imp not in content:
        content = content.replace("import androidx.compose.foundation.layout.*", f"import androidx.compose.foundation.layout.*\n{imp}")

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
