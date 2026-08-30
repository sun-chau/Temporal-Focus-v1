import re

with open("app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt", "r") as f:
    content = f.read()

search_str = r'''            Surface\(
                color = if \(isEarly\) Color\(0xFF4CAF50\)\.copy\(alpha = 0\.15f\) else MaterialTheme\.colorScheme\.error\.copy\(alpha = 0\.15f\),
                shape = CircleShape,
                modifier = Modifier\.border\(1\.dp, if \(isEarly\) Color\(0xFF4CAF50\)\.copy\(alpha = 0\.5f\) else MaterialTheme\.colorScheme\.error\.copy\(alpha = 0\.5f\), CircleShape\)
            \) \{
                Text\(
                    text = if \(isEarly\) "Early by \$diffString" else "Late by \$diffString",
                    style = MaterialTheme\.typography\.labelMedium,
                    color = if \(isEarly\) Color\(0xFF388E3C\) else MaterialTheme\.colorScheme\.error,
                    modifier = Modifier\.padding\(horizontal = 12\.dp, vertical = 4\.dp\),
                    fontWeight = FontWeight\.Bold
                \)
            \}'''

replace_str = '''            val statusText = when {
                isEarly -> "Early by $diffString"
                task.completionStatus == "ON_TIME" -> "On time, marked late"
                task.completionStatus == "LATE" -> "Late by $diffString"
                else -> "Late by $diffString"
            }
            val statusColor = when {
                isEarly -> Color(0xFF388E3C)
                task.completionStatus == "ON_TIME" -> Color(0xFF2196F3)
                else -> MaterialTheme.colorScheme.error
            }
            
            Surface(
                color = statusColor.copy(alpha = 0.15f),
                shape = CircleShape,
                modifier = Modifier.border(1.dp, statusColor.copy(alpha = 0.5f), CircleShape)
            ) {
                Text(
                    text = statusText,
                    style = MaterialTheme.typography.labelMedium,
                    color = statusColor,
                    modifier = Modifier.padding(horizontal = 12.dp, vertical = 4.dp),
                    fontWeight = FontWeight.Bold
                )
            }
            
            if (task.shiftedAmount > 0) {
                Spacer(modifier = Modifier.height(8.dp))
                val shiftDiff = task.shiftedAmount
                val shiftHours = (shiftDiff / (1000 * 60 * 60))
                val shiftMinutes = (shiftDiff / (1000 * 60)) % 60
                val shiftString = String.format(Locale.getDefault(), "%02d:%02d", shiftHours, shiftMinutes)
                Text(
                    text = "Shifted by +$shiftString",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.primary
                )
            }'''

content = re.sub(search_str, replace_str, content)

with open("app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt", "w") as f:
    f.write(content)
