import re

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "r") as f:
    content = f.read()

search_str = r'''                val totalDuration = task\.targetDateTime - task\.createdAt
                val elapsed = currentTime - task\.createdAt
                val percent = if \(totalDuration > 0\) \(\(elapsed\.toFloat\(\) / totalDuration\) \* 100\)\.toInt\(\)\.coerceIn\(0, 100\) else 100
                Text\("\$\{if\(isOverdue\) 100 else percent\}% Elapsed", color = Color\.Gray, fontSize = 12\.sp\)
            \}'''

replace_str = '''                val totalDuration = task.targetDateTime - task.createdAt
                val elapsed = currentTime - task.createdAt
                val percent = if (totalDuration > 0) ((elapsed.toFloat() / totalDuration) * 100).toInt().coerceIn(0, 100) else 100
                
                Row(verticalAlignment = Alignment.CenterVertically) {
                    if (task.shiftedAmount > 0) {
                        val shiftMillis = task.shiftedAmount
                        val shiftHours = (shiftMillis / (1000 * 60 * 60))
                        val shiftMins = (shiftMillis / (1000 * 60)) % 60
                        val shiftStr = if (shiftHours > 0) "+${shiftHours}h ${shiftMins}m" else "+${shiftMins}m"
                        Text(shiftStr, color = MaterialTheme.colorScheme.primary, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.width(8.dp))
                    }
                    Text("${if(isOverdue) 100 else percent}% Elapsed", color = Color.Gray, fontSize = 12.sp)
                }
            }'''

content = re.sub(search_str, replace_str, content)

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "w") as f:
    f.write(content)
