with open('app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt', 'r') as f:
    content = f.read()

# I will just regex remove the lines starting with annually* in clearForm
import re

content = re.sub(r'^\s*annuallyType = AnnuallyType\.DATES\n?', '', content, flags=re.MULTILINE)
content = re.sub(r'^\s*annuallyMonth = Calendar\.JANUARY\n?', '', content, flags=re.MULTILINE)
content = re.sub(r'^\s*annuallyDates = emptySet\(\)\n?', '', content, flags=re.MULTILINE)
content = re.sub(r'^\s*annuallyWeek = 1\n?', '', content, flags=re.MULTILINE)
content = re.sub(r'^\s*annuallyDayOfWeek = Calendar\.SUNDAY\n?', '', content, flags=re.MULTILINE)

with open('app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt', 'w') as f:
    f.write(content)
