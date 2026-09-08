import re

with open("app/src/main/java/com/example/ui/screens/AssignmentTrackerUI.kt", "r") as f:
    content = f.read()

old_calc = """                val daysRemaining = ((task.deadlineEpoch - System.currentTimeMillis()) / (1000 * 60 * 60 * 24)).toInt()"""
new_calc = """                val timeDiffMillis = task.deadlineEpoch - System.currentTimeMillis()
                val hoursRemaining = timeDiffMillis / (1000 * 60 * 60)
                val daysRemaining = hoursRemaining / 24
                val countdownStr = if (java.lang.Math.abs(daysRemaining) > 0) "T-${daysRemaining} DAYS" else "T-${hoursRemaining} HOURS"
                val format = java.text.SimpleDateFormat("dd MMM HH:mm", java.util.Locale.getDefault())
                val absoluteTime = format.format(java.util.Date(task.deadlineEpoch)).uppercase()"""

content = content.replace(old_calc, new_calc)

with open("app/src/main/java/com/example/ui/screens/AssignmentTrackerUI.kt", "w") as f:
    f.write(content)

