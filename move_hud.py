import re

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'r') as f:
    content = f.read()

# 1. Remove AnalyticsWatermark(uiState) from the root Box
old_root = """    Box(modifier = Modifier.fillMaxSize()) {
        AnalyticsWatermark(uiState)
        Column("""

new_root = """    Box(modifier = Modifier.fillMaxSize()) {
        Column("""

content = content.replace(old_root, new_root)

# 2. Insert TacticalStatsGrid(uiState) after the main timer Box
timer_end_regex = r"(\s+)(\s*\}\n\s*\}\n\s*Spacer\(modifier = Modifier\.height\(80\.dp\)\) // space for FAB)"
# Wait, let's find the exact text
old_insert = """                    }
                }
            }
            Spacer(modifier = Modifier.height(80.dp)) // space for FAB
        }"""
new_insert = """                    }
                }
            }
            
            TacticalStatsGrid(uiState)
            
            Spacer(modifier = Modifier.height(80.dp)) // space for FAB
        }"""

content = content.replace(old_insert, new_insert)

# 3. Rename and Refactor AnalyticsWatermark -> TacticalStatsGrid
old_watermark = """@Composable
private fun AnalyticsWatermark(uiState: com.example.viewmodel.UiState) {"""
new_watermark = """@Composable
private fun TacticalStatsGrid(uiState: com.example.viewmodel.UiState) {"""

content = content.replace(old_watermark, new_watermark)

# 4. Modify the styling and Column layout inside TacticalStatsGrid
old_style_and_layout = """    // 4. Ghost Typography
    val textStyle = androidx.compose.ui.text.TextStyle(
        fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace,
        fontWeight = androidx.compose.ui.text.font.FontWeight.Bold,
        fontSize = 22.sp, // Slightly reduced to fit 6 data points cleanly
        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.15f)
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .windowInsetsPadding(WindowInsets.safeDrawing)
            .padding(top = 80.dp, bottom = 48.dp, start = 24.dp, end = 24.dp)
    ) {
        // TOP ROW
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("YIELD: ${uiState.currentSessionCount}/${uiState.pomodoroTargetSessions}", style = textStyle)
            Text("INVESTED: $formattedInvested", style = textStyle)
        }
        
        Spacer(modifier = Modifier.weight(1f))
        
        // MIDDLE ROW
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("INTERVENTIONS: $interventions", style = textStyle)
            Text("EFFICIENCY: $efficiency%", style = textStyle)
        }
        
        Spacer(modifier = Modifier.weight(1f))
        
        // BOTTOM ROW
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("DEVIATION: $formattedDeviation", style = textStyle)
            Text("ETA: $formattedTerminalEta", style = textStyle)
        }
    }"""

new_style_and_layout = """    // 4. Compact Tactical Typography
    val textStyle = androidx.compose.ui.text.TextStyle(
        fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace,
        fontWeight = androidx.compose.ui.text.font.FontWeight.Bold,
        fontSize = 15.sp, // Reduced to fit neatly in a compact grid
        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)
    )

    Column(
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

content = content.replace(old_style_and_layout, new_style_and_layout)

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'w') as f:
    f.write(content)

