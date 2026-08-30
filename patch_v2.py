import re

with open('app/src/main/java/com/example/ui/screens/LandscapeChronographScreen.kt', 'r') as f:
    content = f.read()

# 1. Remove Battery Logic
target1 = """    var batteryPercentage by remember { mutableStateOf(100) }
    
    DisposableEffect(context) {
        val receiver = object : BroadcastReceiver() {
            override fun onReceive(context: Context?, intent: Intent?) {
                if (intent?.action == Intent.ACTION_BATTERY_CHANGED) {
                    val level = intent.getIntExtra(BatteryManager.EXTRA_LEVEL, -1)
                    val scale = intent.getIntExtra(BatteryManager.EXTRA_SCALE, -1)
                    if (level != -1 && scale != -1) {
                        batteryPercentage = (level * 100) / scale
                    }
                }
            }
        }
        val filter = IntentFilter(Intent.ACTION_BATTERY_CHANGED)
        androidx.core.content.ContextCompat.registerReceiver(context, receiver, filter, androidx.core.content.ContextCompat.RECEIVER_NOT_EXPORTED)
        onDispose {
            context.unregisterReceiver(receiver)
        }
    }"""
content = content.replace(target1, "")

# 2. Update Padding
target2 = """    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(backgroundColor)
            .windowInsetsPadding(WindowInsets.safeDrawing)
            .padding(16.dp)
    ) {"""
replacement2 = """    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(backgroundColor)
            .windowInsetsPadding(WindowInsets.safeDrawing)
            .padding(32.dp)
    ) {"""
content = content.replace(target2, replacement2)

# 3. Update onClick in combinedClickable
target3 = """                .combinedClickable(
                    onClick = { is24HourFormat = !is24HourFormat },
                    onLongClick = { isUtilityMode = !isUtilityMode },
                    indication = null,
                    interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() }
                ),"""
replacement3 = """                .combinedClickable(
                    onClick = { },
                    onLongClick = { isUtilityMode = !isUtilityMode },
                    indication = null,
                    interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() }
                ),"""
content = content.replace(target3, replacement3)

# 4. Red Close Button
target4 = """        // Top Left: Close
        IconButton(
            onClick = onBack,
            modifier = Modifier
                .align(Alignment.TopStart)
                .offset { IntOffset(offsetX, offsetY) }
        ) {
            Icon(
                imageVector = Icons.Default.Close,
                contentDescription = "Close",
                tint = textColor,
                modifier = Modifier.size(32.dp)
            )
        }"""
replacement4 = """        // Top Left: Close
        IconButton(
            onClick = onBack,
            modifier = Modifier
                .align(Alignment.TopStart)
                .offset { IntOffset(offsetX, offsetY) }
        ) {
            Icon(
                imageVector = Icons.Default.Close,
                contentDescription = "Close",
                tint = Color.Red,
                modifier = Modifier.size(32.dp)
            )
        }"""
content = content.replace(target4, replacement4)

# 5. Bottom Left Toggle + Remove Top Right Battery
target5_regex = re.compile(r"        // Bottom Left: Theme Toggle.*?\n    }\n}", re.DOTALL)

replacement5 = """        // Bottom Left: Theme & Format Toggle
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier
                .align(Alignment.BottomStart)
                .offset { IntOffset(offsetX, offsetY) }
        ) {
            IconButton(
                onClick = {
                    isDarkMode = !isDarkMode
                    isUtilityMode = false // Reset utility mode on theme change
                }
            ) {
                Icon(
                    imageVector = if (isDarkMode) Icons.Default.LightMode else Icons.Default.DarkMode,
                    contentDescription = "Toggle Theme",
                    tint = textColor,
                    modifier = Modifier.size(32.dp)
                )
            }
            Spacer(modifier = Modifier.width(16.dp))
            Box(
                modifier = Modifier
                    .androidx.compose.ui.draw.clip(androidx.compose.foundation.shape.CircleShape)
                    .androidx.compose.foundation.border(
                        1.dp, 
                        textColor.copy(alpha = 0.5f), 
                        androidx.compose.foundation.shape.CircleShape
                    )
                    .androidx.compose.foundation.clickable { is24HourFormat = !is24HourFormat }
                    .padding(horizontal = 16.dp, vertical = 8.dp),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = if (is24HourFormat) "24" else "12",
                    color = textColor,
                    fontWeight = FontWeight.Bold
                )
            }
        }
    }
}"""
content = re.sub(target5_regex, replacement5, content)

with open('app/src/main/java/com/example/ui/screens/LandscapeChronographScreen.kt', 'w') as f:
    f.write(content)
