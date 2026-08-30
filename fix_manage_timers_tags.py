import re

with open("app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt", "r") as f:
    content = f.read()

# Pass uiState to tabs
content = content.replace("ActiveQueueTab(", "ActiveQueueTab(\n                        uiState = uiState,\n                        viewModel = viewModel,")
content = content.replace("fun ActiveQueueTab(", "fun ActiveQueueTab(\n    uiState: com.example.viewmodel.UiState,\n    viewModel: MainViewModel,")

content = content.replace("CompletedHistoryTab(", "CompletedHistoryTab(\n                        uiState = uiState,\n                        viewModel = viewModel,")
content = content.replace("fun CompletedHistoryTab(", "fun CompletedHistoryTab(\n    uiState: com.example.viewmodel.UiState,\n    viewModel: MainViewModel,")

# Update FilterChips in ActiveQueueTab
# We need to import getTagColor
if "import com.example.ui.utils.getTagColor" not in content:
    content = content.replace("import com.example.ui.screens", "import com.example.ui.screens\nimport com.example.ui.utils.getTagColor")

# It seems the tags themselves are strings, so we can use getTagColor(tag, isDarkTheme, enabled)

search_active_chip_1 = r'''                            androidx.compose.material3.FilterChip\(
                                selected = true,
                                onClick = \{ selectedTags = selectedTags - tag \},
                                label = \{ Text\(tag\) \},
                                leadingIcon = \{
                                    Icon\(Icons.Default.Close, contentDescription = "Remove tag", modifier = Modifier.size\(16.dp\)\)
                                \}
                            \)'''

replace_active_chip_1 = '''                            val isDarkTheme = androidx.compose.foundation.isSystemInDarkTheme()
                            val tagColor = getTagColor(tag, isDarkTheme, uiState.coloredTagsEnabled)
                            androidx.compose.material3.FilterChip(
                                selected = true,
                                onClick = { selectedTags = selectedTags - tag },
                                label = { Text(tag) },
                                leadingIcon = {
                                    Icon(Icons.Default.Close, contentDescription = "Remove tag", modifier = Modifier.size(16.dp))
                                },
                                colors = FilterChipDefaults.filterChipColors(
                                    selectedContainerColor = tagColor.copy(alpha = 0.2f),
                                    selectedLabelColor = tagColor,
                                    selectedLeadingIconColor = tagColor
                                ),
                                border = FilterChipDefaults.filterChipBorder(
                                    borderColor = tagColor.copy(alpha = 0.5f),
                                    selectedBorderColor = tagColor.copy(alpha = 0.5f),
                                    enabled = true,
                                    selected = true
                                )
                            )'''
content = re.sub(search_active_chip_1, replace_active_chip_1, content)

search_active_chip_2 = r'''                            androidx.compose.material3.FilterChip\(
                                selected = false,
                                onClick = \{ selectedTags = selectedTags \+ tag \},
                                label = \{ Text\(tag\) \}
                            \)'''

replace_active_chip_2 = '''                            val isDarkTheme = androidx.compose.foundation.isSystemInDarkTheme()
                            val tagColor = getTagColor(tag, isDarkTheme, uiState.coloredTagsEnabled)
                            androidx.compose.material3.FilterChip(
                                selected = false,
                                onClick = { selectedTags = selectedTags + tag },
                                label = { Text(tag) },
                                colors = FilterChipDefaults.filterChipColors(
                                    containerColor = Color.Transparent,
                                    labelColor = tagColor
                                ),
                                border = FilterChipDefaults.filterChipBorder(
                                    borderColor = tagColor.copy(alpha = 0.5f),
                                    selectedBorderColor = tagColor.copy(alpha = 0.5f),
                                    enabled = true,
                                    selected = false
                                )
                            )'''

content = re.sub(search_active_chip_2, replace_active_chip_2, content)

with open("app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt", "w") as f:
    f.write(content)
