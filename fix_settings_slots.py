import re

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

# Change Main Stage Slots text
content = content.replace('"Main Stage Slots"', '"Chronometer Stage Slots"')
content = content.replace('"Main Stage Slots Configuration"', '"Chronometer Stage Slots Configuration"')
content = content.replace('supportingContent = { Text("Display up to ${uiState.maxStageSlots} timers on the main stage") }', 'supportingContent = { Text("Display " + if (uiState.maxStageSlots == -1) "all" else "up to ${uiState.maxStageSlots} timers") }')

# Now the row for selection
row_old = r'''                        Row\(
                            modifier = Modifier\.fillMaxWidth\(\),
                            horizontalArrangement = Arrangement\.SpaceEvenly
                        \) \{
                            \(1\.\.5\)\.forEach \{ slots ->
                                val isSelected = uiState\.maxStageSlots == slots
                                androidx\.compose\.material3\.Surface\(
                                    modifier = Modifier\.size\(48\.dp\),
                                    shape = androidx\.compose\.foundation\.shape\.CircleShape,
                                    color = if \(isSelected\) MaterialTheme\.colorScheme\.primary else MaterialTheme\.colorScheme\.surfaceVariant,
                                    onClick = \{ 
                                        viewModel\.setMaxStageSlots\(slots\)
                                        showSlotsDialog = false
                                    \}
                                \) \{
                                    androidx\.compose\.foundation\.layout\.Box\(contentAlignment = androidx\.compose\.ui\.Alignment\.Center\) \{
                                        Text\(
                                            text = slots\.toString\(\),
                                            color = if \(isSelected\) MaterialTheme\.colorScheme\.onPrimary else MaterialTheme\.colorScheme\.onSurfaceVariant,
                                            style = MaterialTheme\.typography\.titleMedium,
                                            fontWeight = androidx\.compose\.ui\.text\.font\.FontWeight\.Bold
                                        \)
                                    \}
                                \}
                            \}
                        \}'''

row_new = '''                        var customSlots by remember { mutableStateOf(if (uiState.maxStageSlots > 5) uiState.maxStageSlots.toString() else "") }
                        
                        androidx.compose.foundation.lazy.LazyRow(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            items((1..5).toList()) { slots ->
                                val isSelected = uiState.maxStageSlots == slots
                                androidx.compose.material3.Surface(
                                    modifier = Modifier.size(48.dp),
                                    shape = androidx.compose.foundation.shape.CircleShape,
                                    color = if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                                    onClick = { 
                                        viewModel.setMaxStageSlots(slots)
                                        showSlotsDialog = false
                                    }
                                ) {
                                    androidx.compose.foundation.layout.Box(contentAlignment = androidx.compose.ui.Alignment.Center) {
                                        Text(slots.toString(), color = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)
                                    }
                                }
                            }
                            item {
                                val isSelectedAll = uiState.maxStageSlots == -1
                                androidx.compose.material3.Surface(
                                    modifier = Modifier.height(48.dp).padding(horizontal = 4.dp),
                                    shape = androidx.compose.foundation.shape.RoundedCornerShape(24.dp),
                                    color = if (isSelectedAll) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                                    onClick = { 
                                        viewModel.setMaxStageSlots(-1)
                                        showSlotsDialog = false
                                    }
                                ) {
                                    androidx.compose.foundation.layout.Box(contentAlignment = androidx.compose.ui.Alignment.Center, modifier = Modifier.padding(horizontal = 16.dp)) {
                                        Text("All", color = if (isSelectedAll) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)
                                    }
                                }
                            }
                            item {
                                val isCustomSelected = uiState.maxStageSlots > 5
                                androidx.compose.foundation.layout.Row(verticalAlignment = androidx.compose.ui.Alignment.CenterVertically) {
                                    OutlinedTextField(
                                        value = customSlots,
                                        onValueChange = { customSlots = it.filter { char -> char.isDigit() } },
                                        label = { Text("Custom") },
                                        modifier = Modifier.width(100.dp).padding(start = 8.dp),
                                        singleLine = true,
                                        keyboardOptions = androidx.compose.foundation.text.KeyboardOptions(keyboardType = androidx.compose.ui.text.input.KeyboardType.Number)
                                    )
                                    Spacer(modifier = Modifier.width(8.dp))
                                    androidx.compose.material3.Button(
                                        onClick = {
                                            val parsed = customSlots.toIntOrNull()
                                            if (parsed != null && parsed > 0) {
                                                viewModel.setMaxStageSlots(parsed)
                                                showSlotsDialog = false
                                            }
                                        }
                                    ) {
                                        Text("Set")
                                    }
                                }
                            }
                        }'''

content = re.sub(row_old, row_new, content)
with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)
