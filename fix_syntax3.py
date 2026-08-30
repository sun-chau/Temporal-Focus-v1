import re

with open('app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt', 'r') as f:
    content = f.read()

content = re.sub(r'monthlyDayOfWeek = monthlyDayOfWeek,[\s,]+occurrenceCount = occurrenceCount', 'monthlyDayOfWeek = monthlyDayOfWeek,\n                annuallyType = AnnuallyType.DATES,\n                annuallyMonth = Calendar.JANUARY,\n                annuallyDates = emptySet(),\n                annuallyWeek = 1,\n                annuallyDayOfWeek = Calendar.SUNDAY,\n                occurrenceCount = occurrenceCount', content)

with open('app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt', 'w') as f:
    f.write(content)
