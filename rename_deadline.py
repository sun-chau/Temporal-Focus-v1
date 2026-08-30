import re

files_to_update = [
    "app/src/main/java/com/example/ui/screens/ChronometerScreen.kt",
    "app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt",
    "app/src/main/java/com/example/ui/screens/MainScreen.kt",
    "app/src/main/java/com/example/ui/screens/DeveloperOptionsScreen.kt",
    "app/src/main/java/com/example/ui/screens/LoginScreen.kt",
    "app/src/main/java/com/example/ui/screens/CheckInsScreen.kt",
    "app/src/main/java/com/example/ui/screens/SettingsScreen.kt",
    "app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt"
]

replacements = [
    ("DEADLINES MODE", "REMINDERS MODE"),
    ("Create Deadline", "Create Reminder"),
    ("Target Deadline", "Target Reminder"),
    ("TARGET DEADLINE", "TARGET REMINDER"),
    ("deadline", "reminder"),
    ("Deadline", "Reminder"),
    ("DEADLINES", "REMINDERS"),
    ("Deadlines", "Reminders"),
]

# We should be careful about variable names. We only want to replace text in Strings.
# But "Deadline" in code might be fine to replace if we replace everywhere, but could break if we miss something.
# Let's target only user-facing strings safely.

def process_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # Just replace common UI strings explicitly.
    content = content.replace('"Deadlines"', '"Reminders"')
    content = content.replace('"No active deadlines ticking."', '"No active reminders ticking."')
    content = content.replace('"No active deadlines ticking"', '"No active reminders ticking"')
    content = content.replace('"No deadlines on stage"', '"No reminders on stage"')
    content = content.replace('"Generate a target deadline timer', '"Generate a target reminder timer')
    content = content.replace('"DEADLINES MODE"', '"REMINDERS MODE"')
    content = content.replace('"URGENT QUEUE (NEXT 3 DEADLINE TARGETS)"', '"URGENT QUEUE (NEXT 3 REMINDER TARGETS)"')
    content = content.replace('"Create Deadline"', '"Create Reminder"')
    content = content.replace('"TARGET DEADLINE (ABSOLUTE)"', '"TARGET REMINDER (ABSOLUTE)"')
    content = content.replace('"TARGET DEADLINE"', '"TARGET REMINDER"')
    content = content.replace('"Recurring Deadline"', '"Recurring Reminder"')
    content = content.replace('target deadlines"', 'target reminders"')
    content = content.replace('"Days until deadline (Optional)"', '"Days until reminder (Optional)"')
    content = content.replace('"Deadline Tone"', '"Reminder Tone"')
    content = content.replace('chronometer deadline is reached"', 'chronometer reminder is reached"')
    content = content.replace('"Deadline Vibration"', '"Reminder Vibration"')
    content = content.replace('delete all deadlines', 'delete all reminders')
    content = content.replace('until the deadline"', 'until the reminder"')
    content = content.replace('created deadlines', 'created reminders')
    content = content.replace('Reminder Tone', 'Reminder Tone') # Already done
    content = content.replace('Reminder cannot be after deadline', 'Reminder cannot be after target') # Or target reminder

    with open(filename, 'w') as f:
        f.write(content)

for f in files_to_update:
    process_file(f)

