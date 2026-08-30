import re
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

label_pattern = r"// Content layer \(allowed to bleed horizontally\)\n\s*Row\("
label_replacement = """// Floating Label for Dragging
        if (elevation > 0.dp) {
            val startStrDrag = String.format("%02d:%02d", startCal.get(Calendar.HOUR_OF_DAY), startCal.get(Calendar.MINUTE))
            val endStrDrag = String.format("%02d:%02d", endCal.get(Calendar.HOUR_OF_DAY), endCal.get(Calendar.MINUTE))
            
            Box(
                modifier = Modifier
                    .offset(y = (-24).dp)
                    .align(Alignment.TopCenter)
                    .background(if (isWarning) Color.Red else MaterialTheme.colorScheme.primary, RoundedCornerShape(4.dp))
                    .padding(horizontal = 6.dp, vertical = 2.dp)
            ) {
                Text(
                    text = "$startStrDrag - $endStrDrag",
                    color = MaterialTheme.colorScheme.onPrimary,
                    style = MaterialTheme.typography.labelSmall,
                    fontWeight = FontWeight.Bold
                )
            }
        }
        
        // Content layer (allowed to bleed horizontally)
        Row("""

content = re.sub(label_pattern, label_replacement, content)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
