import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

content = content.replace("import com.example.viewmodel.UiState\n", "import com.example.viewmodel.UiState\nimport com.example.util.parseTerminalCommand\nimport androidx.compose.animation.AnimatedVisibility\nimport java.text.SimpleDateFormat\nimport java.util.Locale\nimport androidx.compose.foundation.text.KeyboardActions\n")

state_target = """    val context = LocalContext.current
    
    var taskName by remember { mutableStateOf("") }
    var deadlineTimeMillis by remember { mutableStateOf<Long?>(null) }"""

state_replacement = """    val context = LocalContext.current
    
    var rawInput by remember { mutableStateOf("") }
    val parsedState by remember { derivedStateOf { parseTerminalCommand(rawInput) } }
    
    var deadlineTimeMillis by remember { mutableStateOf<Long?>(null) }"""
content = content.replace(state_target, state_replacement)

ui_target = """        // The Terminal Input Bar
        Row("""

ui_replacement = """        // The Tactical Feedback HUD
        AnimatedVisibility(visible = parsedState.epochMillis != null || parsedState.priority != "Normal") {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 8.dp, vertical = 4.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                if (parsedState.epochMillis != null) {
                    val format = SimpleDateFormat("HH:mm MMM dd", Locale.getDefault())
                    val timeStr = format.format(parsedState.epochMillis)
                    Text(
                        text = "[ @ $timeStr ]",
                        fontFamily = FontFamily.Monospace,
                        style = MaterialTheme.typography.labelMedium,
                        color = MaterialTheme.colorScheme.primary,
                        modifier = Modifier
                            .border(1.dp, MaterialTheme.colorScheme.primary, RectangleShape)
                            .padding(horizontal = 6.dp, vertical = 2.dp)
                    )
                }
                if (parsedState.priority != "Normal") {
                    val color = if (parsedState.priority == "CRITICAL") MaterialTheme.colorScheme.error else Color(0xFFFFA000) // Amber for MID
                    Text(
                        text = "[ ! ${parsedState.priority} ]",
                        fontFamily = FontFamily.Monospace,
                        style = MaterialTheme.typography.labelMedium,
                        color = color,
                        modifier = Modifier
                            .border(1.dp, color, RectangleShape)
                            .padding(horizontal = 6.dp, vertical = 2.dp)
                    )
                }
            }
        }
        
        // The Terminal Input Bar
        Row("""
content = content.replace(ui_target, ui_replacement)

input_target = """            OutlinedTextField(
                value = taskName,
                onValueChange = { taskName = it },
                modifier = Modifier
                    .weight(1f)
                    .focusRequester(focusRequester),
                placeholder = { 
                    Text(
                        "> QUICK REMINDER...", 
                        fontFamily = FontFamily.Monospace,
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)
                    ) 
                },
                singleLine = true,
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Done),
                shape = RectangleShape,"""

input_replacement = """            OutlinedTextField(
                value = rawInput,
                onValueChange = { rawInput = it },
                modifier = Modifier
                    .weight(1f)
                    .focusRequester(focusRequester),
                placeholder = { 
                    Text(
                        "> QUICK REMINDER...", 
                        fontFamily = FontFamily.Monospace,
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)
                    ) 
                },
                singleLine = true,
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Done),
                keyboardActions = KeyboardActions(
                    onDone = {
                        val finalTime = parsedState.epochMillis ?: deadlineTimeMillis
                        if (parsedState.cleanTitle.isNotBlank()) {
                            viewModel.addQuickDeadline(parsedState.cleanTitle, finalTime, parsedState.priority)
                            rawInput = ""
                            deadlineTimeMillis = null
                        }
                    }
                ),
                shape = RectangleShape,"""
content = content.replace(input_target, input_replacement)

button_target = """            IconButton(
                onClick = {
                    viewModel.addQuickDeadline(taskName, deadlineTimeMillis)
                    taskName = ""
                    deadlineTimeMillis = null
                },
                enabled = taskName.isNotBlank()
            ) {
                Icon(
                    imageVector = Icons.AutoMirrored.Filled.Send, 
                    contentDescription = "Save",
                    tint = if (taskName.isNotBlank()) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface.copy(alpha = 0.3f)
                )
            }"""

button_replacement = """            IconButton(
                onClick = {
                    val finalTime = parsedState.epochMillis ?: deadlineTimeMillis
                    viewModel.addQuickDeadline(parsedState.cleanTitle, finalTime, parsedState.priority)
                    rawInput = ""
                    deadlineTimeMillis = null
                },
                enabled = parsedState.cleanTitle.isNotBlank()
            ) {
                Icon(
                    imageVector = Icons.AutoMirrored.Filled.Send, 
                    contentDescription = "Save",
                    tint = if (parsedState.cleanTitle.isNotBlank()) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface.copy(alpha = 0.3f)
                )
            }"""
content = content.replace(button_target, button_replacement)

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
print("Patched HomeScreen")
