import re

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'r') as f:
    content = f.read()

# 1. State changes
old_state = """    var showSettingsDialog by remember { mutableStateOf(false) }
    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)"""
new_state = """    var showSettingsDialog by remember { mutableStateOf(false) }
    var showInfoSheet by remember { mutableStateOf(false) }
    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    val infoSheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)"""
content = content.replace(old_state, new_state)

# 2. Update TacticalStatsGrid call
old_call = """            TacticalStatsGrid(uiState)"""
new_call = """            TacticalStatsGrid(uiState, onInfoClick = { showInfoSheet = true })"""
content = content.replace(old_call, new_call)

# 3. Add ModalBottomSheet for infoSheet
# Find where showSettingsDialog block ends... actually, let's just insert it before `    }` (end of PomodoroScreen)
# We can search for `    }\n}\n\n@Composable\nfun RepeatingIconButton`
old_end_screen = """            }
        }
    }
}

@Composable
fun RepeatingIconButton"""
new_end_screen = """            }
        }
        
        if (showInfoSheet) {
            ModalBottomSheet(
                onDismissRequest = { showInfoSheet = false },
                sheetState = infoSheetState,
                containerColor = MaterialTheme.colorScheme.surface,
                tonalElevation = 8.dp
            ) {
                TacticalInfoSheetContent()
            }
        }
    }
}

@Composable
fun RepeatingIconButton"""
content = content.replace(old_end_screen, new_end_screen)

# 4. Modify TacticalStatsGrid signature
old_sig = """private fun TacticalStatsGrid(uiState: com.example.viewmodel.UiState) {"""
new_sig = """private fun TacticalStatsGrid(uiState: com.example.viewmodel.UiState, onInfoClick: () -> Unit) {"""
content = content.replace(old_sig, new_sig)

# 5. Insert Info Icon
old_grid_end = """        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("ETA", style = textStyle)
            Text(formattedTerminalEta, style = textStyle)
        }
    }"""
new_grid_end = """        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("ETA", style = textStyle)
            Text(formattedTerminalEta, style = textStyle)
        }
        Spacer(modifier = Modifier.height(4.dp))
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.Center) {
            IconButton(onClick = onInfoClick) {
                Icon(
                    imageVector = Icons.Default.Info,
                    contentDescription = "HUD Info",
                    tint = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.15f),
                    modifier = Modifier.size(24.dp)
                )
            }
        }
    }"""
content = content.replace(old_grid_end, new_grid_end)

# 6. Add new Composable functions at the end of the file
new_components = """

@Composable
fun TacticalInfoSheetContent() {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 24.dp)
            .padding(bottom = 32.dp, top = 8.dp)
            .navigationBarsPadding()
            .verticalScroll(rememberScrollState())
    ) {
        Text(
            "TACTICAL HUD METRICS",
            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f),
            fontSize = 12.sp,
            fontWeight = FontWeight.Bold
        )
        Spacer(Modifier.height(16.dp))
        
        InfoAccordionItem("YIELD", "Tracks your current session progress against your total goal.", "Current Session / Total Target Sessions")
        InfoAccordionItem("INVESTED", "The total accumulated time you have spent strictly in the focus phase.", "Total Focus Time (formatted to HH:mm)")
        InfoAccordionItem("INTERVENTIONS", "A discipline tracker measuring how many times you manually altered the timer during a live session.", "Count of live adjustment actions")
        InfoAccordionItem("EFFICIENCY", "Your focus-to-rest ratio expressed as a percentage.", "(Total Focus Time / Total Elapsed Active Time) * 100")
        InfoAccordionItem("DEVIATION", "The overall schedule drift. It mathematically compares your actual elapsed time against a perfect, uninterrupted schedule.", "(Actual Elapsed Time - Ideal Schedule Elapsed Time) in Minutes")
        InfoAccordionItem("ETA", "The estimated real-world time your entire multi-session block will be completed.", "Current Time + Remaining Current Phase Time + All Future Pending Sessions")
    }
}

@Composable
fun InfoAccordionItem(title: String, description: String, formula: String) {
    var expanded by remember { mutableStateOf(false) }
    Column(modifier = Modifier.fillMaxWidth().clickable { expanded = !expanded }.padding(vertical = 12.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
            Text(title, fontFamily = FontFamily.Monospace, fontWeight = FontWeight.Bold, fontSize = 16.sp)
            Icon(
                imageVector = if (expanded) Icons.Default.ExpandLess else Icons.Default.ExpandMore, 
                contentDescription = null, 
                tint = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)
            )
        }
        if (expanded) {
            Column(modifier = Modifier.padding(top = 8.dp)) {
                Text(description, fontSize = 14.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Spacer(Modifier.height(4.dp))
                Text("Formula: $formula", fontSize = 12.sp, fontFamily = FontFamily.Monospace, color = MaterialTheme.colorScheme.primary)
            }
        }
    }
    HorizontalDivider(color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f))
}
"""

content += new_components

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'w') as f:
    f.write(content)
