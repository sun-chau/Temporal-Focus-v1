import re

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'r') as f:
    content = f.read()

# 1. Update the Row to include SystemTimeBar()
old_row = """                IconButton(onClick = onMenuClick, modifier = Modifier.offset(x = (-12).dp)) {
                    Icon(
                        imageVector = Icons.Default.Menu,
                        contentDescription = "Menu",
                        modifier = Modifier.size(28.dp),
                        tint = MaterialTheme.colorScheme.onSurface
                    )
                }
                IconButton(onClick = { showSettingsDialog = true }, modifier = Modifier.offset(x = 12.dp)) {"""

new_row = """                IconButton(onClick = onMenuClick, modifier = Modifier.offset(x = (-12).dp)) {
                    Icon(
                        imageVector = Icons.Default.Menu,
                        contentDescription = "Menu",
                        modifier = Modifier.size(28.dp),
                        tint = MaterialTheme.colorScheme.onSurface
                    )
                }
                
                SystemTimeBar()
                
                IconButton(onClick = { showSettingsDialog = true }, modifier = Modifier.offset(x = 12.dp)) {"""

content = content.replace(old_row, new_row)

# 2. Append the SystemTimeBar composable
time_bar_code = """
@Composable
fun SystemTimeBar() {
    var currentTime by remember { mutableLongStateOf(System.currentTimeMillis()) }
    
    LaunchedEffect(Unit) {
        while (true) {
            kotlinx.coroutines.delay(1000)
            currentTime = System.currentTimeMillis()
        }
    }
    
    val formatter = remember { java.text.SimpleDateFormat("EEE, MMM d  •  hh:mm a", java.util.Locale.getDefault()) }
    
    Box(
        modifier = Modifier
            .clip(RoundedCornerShape(50))
            .background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
            .padding(horizontal = 16.dp, vertical = 6.dp),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = formatter.format(java.util.Date(currentTime)).uppercase(),
            fontFamily = FontFamily.Monospace,
            fontWeight = FontWeight.Bold,
            fontSize = 11.sp,
            letterSpacing = 1.sp,
            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.8f)
        )
    }
}
"""

content += time_bar_code

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'w') as f:
    f.write(content)
