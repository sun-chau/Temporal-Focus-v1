import re

with open('app/src/main/java/com/example/receiver/TimerAlarmReceiver.kt', 'r') as f:
    content = f.read()

bad_notification_building = """            if (isApproaching) {
                builder.setContentTitle("Upcoming: $taskName")
                builder.setContentText("Ends in $offsetMinutes minutes.")
                builder.setPriority(NotificationCompat.PRIORITY_DEFAULT)
                
                val bigTextStyle = NotificationCompat.BigTextStyle()
                if (task.description.isNullOrEmpty()) {
                    bigTextStyle.bigText("Ends in $offsetMinutes minutes.")
                } else {
                    bigTextStyle.bigText("${task.name}\\n${task.description}")
                }
                builder.setStyle(bigTextStyle)
                builder.addAction(R.drawable.ic_launcher_foreground, "Mark Complete", pendingCompleteIntent)
                builder.addAction(R.drawable.ic_launcher_foreground, "Snooze", pendingSnoozeIntent)
            } else {
                builder.setContentTitle("Time's Up!")
                builder.setContentText("\\"$taskName\\" has reached its target time.")
                builder.setPriority(NotificationCompat.PRIORITY_HIGH)
                
                builder.addAction(R.drawable.ic_launcher_foreground, "View Details", pendingOpenIntent)
                builder.addAction(R.drawable.ic_launcher_foreground, "Mark Complete", pendingCompleteIntent)
            }"""

good_notification_building = """            if (isDeadline) {
                builder.setContentTitle("Deadline: $taskName")
                builder.setContentText("Due now!")
                builder.setPriority(NotificationCompat.PRIORITY_HIGH)
                builder.addAction(R.drawable.ic_launcher_foreground, "View Details", pendingOpenIntent)
                builder.addAction(R.drawable.ic_launcher_foreground, "Mark Complete", pendingCompleteIntent)
            } else if (isApproaching) {
                builder.setContentTitle("Upcoming: $taskName")
                builder.setContentText("Ends in $offsetMinutes minutes.")
                builder.setPriority(NotificationCompat.PRIORITY_DEFAULT)
                
                val bigTextStyle = NotificationCompat.BigTextStyle()
                if (task.description.isNullOrEmpty()) {
                    bigTextStyle.bigText("Ends in $offsetMinutes minutes.")
                } else {
                    bigTextStyle.bigText("${task.name}\\n${task.description}")
                }
                builder.setStyle(bigTextStyle)
                builder.addAction(R.drawable.ic_launcher_foreground, "Mark Complete", pendingCompleteIntent)
                builder.addAction(R.drawable.ic_launcher_foreground, "Snooze", pendingSnoozeIntent)
            } else {
                builder.setContentTitle("Time's Up!")
                builder.setContentText("\\"$taskName\\" has reached its target time.")
                builder.setPriority(NotificationCompat.PRIORITY_HIGH)
                
                builder.addAction(R.drawable.ic_launcher_foreground, "View Details", pendingOpenIntent)
                builder.addAction(R.drawable.ic_launcher_foreground, "Mark Complete", pendingCompleteIntent)
            }"""

content = content.replace(bad_notification_building, good_notification_building)

with open('app/src/main/java/com/example/receiver/TimerAlarmReceiver.kt', 'w') as f:
    f.write(content)
