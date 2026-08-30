import re

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

search_str = r'''                        androidx\.compose\.foundation\.lazy\.LazyRow\(
                            modifier = Modifier\.fillMaxWidth\(\),
                            horizontalArrangement = Arrangement\.spacedBy\(12\.dp\)
                        \) \{
                            items\(\(1\.\.5\)\.toList\(\), key = \{ it \}\) \{ slots ->
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
                                        Text\(slots\.toString\(\), color = if \(isSelected\) MaterialTheme\.colorScheme\.onPrimary else MaterialTheme\.colorScheme\.onSurfaceVariant, fontWeight = androidx\.compose\.ui\.text\.font\.FontWeight\.Bold\)
                                    \}
                                \}
                            \}
                            item \{
                                val isSelectedAll = uiState\.maxStageSlots == -1
                                androidx\.compose\.material3\.Surface\(
                                    modifier = Modifier\.height\(48\.dp\)\.padding\(horizontal = 4\.dp\),
                                    shape = androidx\.compose\.foundation\.shape\.RoundedCornerShape\(24\.dp\),
                                    color = if \(isSelectedAll\) MaterialTheme\.colorScheme\.primary else MaterialTheme\.colorScheme\.surfaceVariant,
                                    onClick = \{ 
                                        viewModel\.setMaxStageSlots\(-1\)
                                        showSlotsDialog = false
                                    \}
                                \) \{
                                    androidx\.compose\.foundation\.layout\.Box\(contentAlignment = androidx\.compose\.ui\.Alignment\.Center, modifier = Modifier\.padding\(horizontal = 16\.dp\)\) \{
                                        Text\("All", color = if \(isSelectedAll\) MaterialTheme\.colorScheme\.onPrimary else MaterialTheme\.colorScheme\.onSurfaceVariant, fontWeight = androidx\.compose\.ui\.text\.font\.FontWeight\.Bold\)
                                    \}
                                \}
                            \}
                            item \{
                                val isCustomSelected = uiState\.maxStageSlots > 5
                                androidx\.compose\.foundation\.layout\.Row\(verticalAlignment = androidx\.compose\.ui\.Alignment\.CenterVertically\) \{
                                    OutlinedTextField\(
                                        value = customSlots,
                                        onValueChange = \{ customSlots = it\.filter \{ char -> char\.isDigit\(\) \} \},
                                        label = \{ Text\("Custom"\) \},
                                        modifier = Modifier\.width\(100\.dp\)\.padding\(start = 8\.dp\),
                                        singleLine = true,
                                        keyboardOptions = androidx\.compose\.foundation\.text\.KeyboardOptions\(keyboardType = androidx\.compose\.ui\.text\.input\.KeyboardType\.Number\)
                                    \)
                                    Spacer\(modifier = Modifier\.width\(8\.dp\)\)
                                    androidx\.compose\.material3\.Button\(
                                        onClick = \{
                                            val parsed = customSlots\.toIntOrNull\(\)
                                            if \(parsed != null && parsed > 0\) \{
                                                viewModel\.setMaxStageSlots\(parsed\)
                                                showSlotsDialog = false
                                            \}
                                        \}
                                    \) \{
                                        Text\("Set"\)
                                    \}
                                \}
                            \}
                        \}'''

replace_str = '''                        @OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)
                        androidx.compose.foundation.layout.FlowRow(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(12.dp),
                            verticalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            (1..5).forEach { slots ->
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
                        }'''

content = re.sub(search_str, replace_str, content)
with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)
