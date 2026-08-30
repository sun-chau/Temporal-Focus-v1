import re

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "r") as f:
    content = f.read()

search_str = r'''                            Text\("Target Date: \$\{SimpleDateFormat\("MMM dd, yyyy hh:mm a", Locale\.getDefault\(\)\)\.format\(Date\(task\.targetDateTime\)\)\}", color = Color\.Gray, fontSize = 14\.sp\)
                            
                            val recurrenceRule'''

replace_str = '''                            Text("Target Date: ${SimpleDateFormat("MMM dd, yyyy hh:mm a", Locale.getDefault()).format(Date(task.targetDateTime))}", color = Color.Gray, fontSize = 14.sp)
                            
                            if (task.shiftedAmount > 0) {
                                val shiftMillis = task.shiftedAmount
                                val shiftHours = (shiftMillis / (1000 * 60 * 60))
                                val shiftMins = (shiftMillis / (1000 * 60)) % 60
                                val shiftStr = if (shiftHours > 0) "+${shiftHours}h ${shiftMins}m" else "+${shiftMins}m"
                                Text("Shifted: $shiftStr", color = MaterialTheme.colorScheme.primary, fontSize = 14.sp)
                            }
                            
                            val recurrenceRule'''

content = re.sub(search_str, replace_str, content)

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "w") as f:
    f.write(content)
