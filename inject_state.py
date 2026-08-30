import re
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

state_vars = """
    val haptic = LocalHapticFeedback.current
    
    // Task Drag State
    var dragTaskId by remember { mutableStateOf<String?>(null) }
    var dragStartTimeMillis by remember { mutableStateOf(0L) }
    var dragEndTimeMillis by remember { mutableStateOf(0L) }
    var dragLaneIndex by remember { mutableStateOf(0) }
    var dragOriginalLane by remember { mutableStateOf(0) }
    var isDragColliding by remember { mutableStateOf(false) }
    var accumulatedDragX by remember { mutableStateOf(0f) }
    var accumulatedDragY by remember { mutableStateOf(0f) }
    
    // Ghost Block State
    var isCreatingGhost by remember { mutableStateOf(false) }
    var ghostStartTimeMillis by remember { mutableStateOf(0L) }
    var ghostEndTimeMillis by remember { mutableStateOf(0L) }
    var ghostLaneIndex by remember { mutableStateOf(0) }
    var ghostInitialDragX by remember { mutableStateOf(0f) }
    var isGhostColliding by remember { mutableStateOf(false) }
"""

content = content.replace("val todayScrollState = rememberScrollState()", state_vars + "\n    val todayScrollState = rememberScrollState()")

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
