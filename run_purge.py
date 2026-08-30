import re

with open('app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt', 'r') as f:
    content = f.read()

# 1. Variables
content = re.sub(r'\s*var dailyInterval.*?\{.*?\n', '\n', content)
content = re.sub(r'\s*var weeklyDays.*?\{.*?\n', '\n', content)
content = re.sub(r'\s*var dailyMinusHolding.*?\{.*?\n', '\n', content)
content = re.sub(r'\s*var dailyPlusHolding.*?\{.*?\n', '\n', content)

# 2. Default Type Shift
content = content.replace(
    'var recurrenceType by remember { mutableStateOf(RecurrenceType.DAILY) }',
    'var recurrenceType by remember { mutableStateOf(RecurrenceType.MONTHLY) }'
)

# 3. Coroutines
content = re.sub(r'\s*LaunchedEffect\(dailyMinusHolding\)\s*\{[^\}]*\}[^\}]*\}[^\}]*\}', '', content)
content = re.sub(r'\s*LaunchedEffect\(dailyPlusHolding\)\s*\{[^\}]*\}[^\}]*\}[^\}]*\}', '', content)

# 4. Dynamic String Update
content = content.replace(
    'isRecurring, recurrenceType, dailyInterval, weeklyDays,',
    'isRecurring, recurrenceType,'
)

# dynamic string when block
daily_weekly_str_pattern = r'\s*RecurrenceType\.DAILY -> \{\s*if \(dailyInterval == 1\) "Repeats every day\$countStr"\s*else "Repeats every \$dailyInterval days\$countStr"\s*\}\s*RecurrenceType\.WEEKLY -> \{\s*if \(weeklyDays\.isEmpty\(\)\) "Repeats weekly on no days\$countStr"\s*else \{\s*val daysStr = weeklyDays\.sorted\(\)\.joinToString\([^\n]+\n\s*"Repeats weekly on \$daysStr\$countStr"\s*\}\s*\}'
content = re.sub(daily_weekly_str_pattern, '', content)

# 5. Data Payload Alignment (Save Function)
content = content.replace('dailyInterval = dailyInterval,', 'dailyInterval = 1,')
content = content.replace('weeklyDays = weeklyDays,', 'weeklyDays = emptySet(),')

# 6. TabRow
old_tab_row = """                    ScrollableTabRow(
                        selectedTabIndex = when (recurrenceType) {
                            RecurrenceType.DAILY -> 0
                            RecurrenceType.WEEKLY -> 1
                            RecurrenceType.MONTHLY -> 2
                            RecurrenceType.ANNUALLY -> 3
                            else -> 0
                        },
                        edgePadding = 0.dp
                    ) {
                        Tab(selected = recurrenceType == RecurrenceType.DAILY, onClick = { recurrenceType = RecurrenceType.DAILY }) { Text("Daily", modifier = Modifier.padding(16.dp)) }
                        Tab(selected = recurrenceType == RecurrenceType.WEEKLY, onClick = { recurrenceType = RecurrenceType.WEEKLY }) { Text("Weekly", modifier = Modifier.padding(16.dp)) }
                        Tab(selected = recurrenceType == RecurrenceType.MONTHLY, onClick = { recurrenceType = RecurrenceType.MONTHLY }) { Text("Monthly", modifier = Modifier.padding(16.dp)) }
                        Tab(selected = recurrenceType == RecurrenceType.ANNUALLY, onClick = { recurrenceType = RecurrenceType.ANNUALLY }) { Text("Annually", modifier = Modifier.padding(16.dp)) }
                    }"""
                    
new_tab_row = """                    ScrollableTabRow(
                        selectedTabIndex = when (recurrenceType) {
                            RecurrenceType.MONTHLY -> 0
                            RecurrenceType.ANNUALLY -> 1
                            else -> 0
                        },
                        edgePadding = 0.dp
                    ) {
                        Tab(selected = recurrenceType == RecurrenceType.MONTHLY, onClick = { recurrenceType = RecurrenceType.MONTHLY }) { Text("Monthly", modifier = Modifier.padding(16.dp)) }
                        Tab(selected = recurrenceType == RecurrenceType.ANNUALLY, onClick = { recurrenceType = RecurrenceType.ANNUALLY }) { Text("Annually", modifier = Modifier.padding(16.dp)) }
                    }"""

content = content.replace(old_tab_row, new_tab_row)

# 7. UI Layout Blocks (at the bottom)
# Delete RecurrenceType.DAILY -> { ... } and RecurrenceType.WEEKLY -> { ... }
ui_blocks_pattern = r'\s*RecurrenceType\.DAILY -> \{.*?(?=RecurrenceType\.MONTHLY -> \{)'
content = re.sub(ui_blocks_pattern, '\n                    ', content, flags=re.DOTALL)


with open('app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt', 'w') as f:
    f.write(content)

