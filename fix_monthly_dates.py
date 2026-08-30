with open('app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt', 'r') as f:
    content = f.read()

bad_if_block = """                                    if (monthlyDates.size == 31) {
                                        recurrenceType = RecurrenceType.DAILY
                                        dailyInterval = 1
                                    }"""
content = content.replace(bad_if_block, "")

with open('app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt', 'w') as f:
    f.write(content)
