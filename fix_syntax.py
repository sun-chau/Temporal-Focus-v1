import re

with open('app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt', 'r') as f:
    content = f.read()

# Fix saveDraft
bad_save_draft = """                monthlyWeek = monthlyWeek,
                monthlyDayOfWeek = monthlyDayOfWeek,
,,,,
                occurrenceCount = occurrenceCount"""

good_save_draft = """                monthlyWeek = monthlyWeek,
                monthlyDayOfWeek = monthlyDayOfWeek,
                annuallyType = AnnuallyType.DATES,
                annuallyMonth = Calendar.JANUARY,
                annuallyDates = emptySet(),
                annuallyWeek = 1,
                annuallyDayOfWeek = Calendar.SUNDAY,
                occurrenceCount = occurrenceCount"""

content = content.replace(bad_save_draft, good_save_draft)


# Fix finalDraft
bad_final_draft = """                            monthlyWeek = monthlyWeek, monthlyDayOfWeek = monthlyDayOfWeek,
, annuallyMonth = Calendar.JANUARY, annuallyDates = emptySet(),
, annuallyDayOfWeek = Calendar.SUNDAY,
                            occurrenceCount = occurrenceCount"""

good_final_draft = """                            monthlyWeek = monthlyWeek, monthlyDayOfWeek = monthlyDayOfWeek,
                            annuallyType = AnnuallyType.DATES, annuallyMonth = Calendar.JANUARY, annuallyDates = emptySet(),
                            annuallyWeek = 1, annuallyDayOfWeek = Calendar.SUNDAY,
                            occurrenceCount = occurrenceCount"""

content = content.replace(bad_final_draft, good_final_draft)

with open('app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt', 'w') as f:
    f.write(content)
