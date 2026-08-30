import re

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'r') as f:
    content = f.read()

old_layout = """    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(top = 24.dp, bottom = 24.dp, start = 8.dp, end = 8.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        // TOP ROW
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("YIELD: ${uiState.currentSessionCount}/${uiState.pomodoroTargetSessions}", style = textStyle)
            Text("INVESTED: $formattedInvested", style = textStyle)
        }
        
        // MIDDLE ROW
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("INTERVENTIONS: $interventions", style = textStyle)
            Text("EFFICIENCY: $efficiency%", style = textStyle)
        }
        
        // BOTTOM ROW
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("DEVIATION: $formattedDeviation", style = textStyle)
            Text("ETA: $formattedTerminalEta", style = textStyle)
        }
    }"""

new_layout = """    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(top = 24.dp, bottom = 24.dp, start = 32.dp, end = 32.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("YIELD", style = textStyle)
            Text("${uiState.currentSessionCount}/${uiState.pomodoroTargetSessions}", style = textStyle)
        }
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("INVESTED", style = textStyle)
            Text(formattedInvested, style = textStyle)
        }
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("INTERVENTIONS", style = textStyle)
            Text("$interventions", style = textStyle)
        }
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("EFFICIENCY", style = textStyle)
            Text("$efficiency%", style = textStyle)
        }
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("DEVIATION", style = textStyle)
            Text(formattedDeviation, style = textStyle)
        }
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("ETA", style = textStyle)
            Text(formattedTerminalEta, style = textStyle)
        }
    }"""

content = content.replace(old_layout, new_layout)

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'w') as f:
    f.write(content)
