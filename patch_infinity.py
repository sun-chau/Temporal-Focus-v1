import re

with open("app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Add imports
imports_to_add = """import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.ui.input.pointer.pointerInput
import kotlinx.coroutines.delay
"""

content = content.replace("import androidx.compose.foundation.background", imports_to_add + "import androidx.compose.foundation.background")

# Fix occurrenceCount state variable definition to just find where it's defined and append LaunchedEffects
search_occurrence = "    var occurrenceCount by remember { mutableStateOf(draft.occurrenceCount) }"
replace_occurrence = """    var occurrenceCount by remember { mutableStateOf(draft.occurrenceCount) }
    
    var minusHolding by remember { mutableStateOf(false) }
    var plusHolding by remember { mutableStateOf(false) }

    LaunchedEffect(minusHolding) {
        if (minusHolding) {
            if (occurrenceCount > 0) occurrenceCount--
            delay(500)
            while (minusHolding && occurrenceCount > 0) {
                occurrenceCount--
                delay(100)
            }
        }
    }

    LaunchedEffect(plusHolding) {
        if (plusHolding) {
            occurrenceCount++
            delay(500)
            while (plusHolding) {
                occurrenceCount++
                delay(100)
            }
        }
    }"""
content = content.replace(search_occurrence, replace_occurrence)

# Fix count string
search_countstr = 'val countStr = if (occurrenceCount > 1) " for $occurrenceCount occurrences." else " once."'
replace_countstr = 'val countStr = if (occurrenceCount <= 0) " indefinitely." else if (occurrenceCount > 1) " for $occurrenceCount occurrences." else " once."'
content = content.replace(search_countstr, replace_countstr)

# Replace the UI row
search_ui = """                // Recurrence Count
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("Number of occurrences: ")
                    IconButton(onClick = { if (occurrenceCount > 1) occurrenceCount-- }) { Text("-", fontSize = 24.sp) }
                    Text("$occurrenceCount")
                    IconButton(onClick = { occurrenceCount++ }) { Text("+", fontSize = 24.sp) }
                }"""

replace_ui = """                // Recurrence Count
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("Number of occurrences: ")
                    Box(
                        modifier = Modifier
                            .padding(8.dp)
                            .pointerInput(Unit) {
                                detectTapGestures(
                                    onPress = {
                                        minusHolding = true
                                        tryAwaitRelease()
                                        minusHolding = false
                                    }
                                )
                            }
                    ) {
                        Text("-", fontSize = 24.sp, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                    }
                    
                    Text(if (occurrenceCount <= 0) "∞" else "$occurrenceCount", fontWeight = FontWeight.Bold)
                    
                    Box(
                        modifier = Modifier
                            .padding(8.dp)
                            .pointerInput(Unit) {
                                detectTapGestures(
                                    onPress = {
                                        plusHolding = true
                                        tryAwaitRelease()
                                        plusHolding = false
                                    }
                                )
                            }
                    ) {
                        Text("+", fontSize = 24.sp, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                    }
                }"""
content = content.replace(search_ui, replace_ui)

with open("app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt", "w") as f:
    f.write(content)
