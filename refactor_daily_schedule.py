import re

with open('app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt', 'r') as f:
    content = f.read()

# 1. State Variable Purge
content = re.sub(r'\s*var annuallyType by remember \{ mutableStateOf\(draft\.annuallyType\) \}', '', content)
content = re.sub(r'\s*var annuallyMonth by remember \{ mutableStateOf\(draft\.annuallyMonth\) \}', '', content)
content = re.sub(r'\s*var annuallyDates by remember \{ mutableStateOf\(draft\.annuallyDates\) \}', '', content)
content = re.sub(r'\s*var annuallyWeek by remember \{ mutableStateOf\(draft\.annuallyWeek\) \}', '', content)
content = re.sub(r'\s*var annuallyDayOfWeek by remember \{ mutableStateOf\(draft\.annuallyDayOfWeek\) \}', '', content)

# 2. Dynamic String Update
content = content.replace(
    'annuallyType, annuallyMonth, annuallyDates, annuallyWeek, annuallyDayOfWeek, occurrenceCount',
    'occurrenceCount'
)

# Remove RecurrenceType.ANNUALLY block in dynamic string
annually_string_pattern = r'\s*RecurrenceType\.ANNUALLY -> \{.*?\n\s*"Repeats annually on \$condition\$countStr"\s*\}'
content = re.sub(annually_string_pattern, '', content, flags=re.DOTALL)

# 3. TabRow Update
old_tab_row = """                ScrollableTabRow(
                    selectedTabIndex = when (recurrenceType) {
                        RecurrenceType.DAILY -> 0
                        RecurrenceType.WEEKLY -> 1
                        RecurrenceType.MONTHLY -> 2
                        RecurrenceType.ANNUALLY -> 3
                        else -> 0
                    },
                    edgePadding = 0.dp
                ) {
                    Tab(selected = recurrenceType == RecurrenceType.DAILY, onClick = { recurrenceType = RecurrenceType.DAILY }, text = { Text("Daily") })
                    Tab(selected = recurrenceType == RecurrenceType.WEEKLY, onClick = { recurrenceType = RecurrenceType.WEEKLY }, text = { Text("Weekly") })
                    Tab(selected = recurrenceType == RecurrenceType.MONTHLY, onClick = { recurrenceType = RecurrenceType.MONTHLY }, text = { Text("Monthly") })
                    Tab(selected = recurrenceType == RecurrenceType.ANNUALLY, onClick = { recurrenceType = RecurrenceType.ANNUALLY }, text = { Text("Annually") })
                }"""

new_tab_row = """                ScrollableTabRow(
                    selectedTabIndex = when (recurrenceType) {
                        RecurrenceType.DAILY -> 0
                        RecurrenceType.WEEKLY -> 1
                        RecurrenceType.MONTHLY -> 2
                        else -> 0
                    },
                    edgePadding = 0.dp
                ) {
                    Tab(selected = recurrenceType == RecurrenceType.DAILY, onClick = { recurrenceType = RecurrenceType.DAILY }, text = { Text("Daily") })
                    Tab(selected = recurrenceType == RecurrenceType.WEEKLY, onClick = { recurrenceType = RecurrenceType.WEEKLY }, text = { Text("Weekly") })
                    Tab(selected = recurrenceType == RecurrenceType.MONTHLY, onClick = { recurrenceType = RecurrenceType.MONTHLY }, text = { Text("Monthly") })
                }"""

content = content.replace(old_tab_row, new_tab_row)

# 4. Remove RecurrenceType.ANNUALLY block in UI Layout
ui_blocks_pattern = r'\s*RecurrenceType\.ANNUALLY -> \{.*?(?=\s*else -> \{\})'
content = re.sub(ui_blocks_pattern, '\n                    ', content, flags=re.DOTALL)

# 5. Data Payload Alignment
# saveDraft lambda
content = re.sub(r'annuallyType\s*=\s*annuallyType,', 'annuallyType = AnnuallyType.DATES,', content)
content = re.sub(r'annuallyMonth\s*=\s*annuallyMonth,', 'annuallyMonth = Calendar.JANUARY,', content)
content = re.sub(r'annuallyDates\s*=\s*annuallyDates,', 'annuallyDates = emptySet(),', content)
content = re.sub(r'annuallyWeek\s*=\s*annuallyWeek,', 'annuallyWeek = 1,', content)
content = re.sub(r'annuallyDayOfWeek\s*=\s*annuallyDayOfWeek,', 'annuallyDayOfWeek = Calendar.SUNDAY,', content)
# Check for occurrences like `annuallyDayOfWeek = annuallyDayOfWeek` inside the final draft creation which might lack commas at the end
content = re.sub(r'annuallyType\s*=\s*annuallyType', 'annuallyType = AnnuallyType.DATES', content)
content = re.sub(r'annuallyMonth\s*=\s*annuallyMonth', 'annuallyMonth = Calendar.JANUARY', content)
content = re.sub(r'annuallyDates\s*=\s*annuallyDates', 'annuallyDates = emptySet()', content)
content = re.sub(r'annuallyWeek\s*=\s*annuallyWeek', 'annuallyWeek = 1', content)
content = re.sub(r'annuallyDayOfWeek\s*=\s*annuallyDayOfWeek', 'annuallyDayOfWeek = Calendar.SUNDAY', content)


with open('app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt', 'w') as f:
    f.write(content)
