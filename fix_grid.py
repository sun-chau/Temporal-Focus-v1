import re

with open('app/src/main/java/com/example/ui/screens/ColorCustomizationScreen.kt', 'r') as f:
    content = f.read()

# Replace LazyVerticalGrid with a Column of Rows
old_grid = """            LazyVerticalGrid(
                columns = GridCells.Fixed(2),
                modifier = Modifier
                    .fillMaxWidth()
                    .height(240.dp)
                    .padding(horizontal = 12.dp),
                contentPadding = PaddingValues(bottom = 16.dp)
            ) {
                val isSystemDark = androidx.compose.foundation.isSystemInDarkTheme()
            val isDark = when (uiState.appearanceMode) {
                1 -> false
                2 -> true
                else -> isSystemDark
            }
            items(getPreMadeThemes(isDark)) { theme ->
                    ThemeCard(
                        theme = theme,
                        selected = uiState.currentTheme == theme.name,
                        onClick = { viewModel.setTheme(theme.name) }
                    )
                }
            }"""

new_grid = """            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 12.dp)
            ) {
                val isSystemDark = androidx.compose.foundation.isSystemInDarkTheme()
                val isDark = when (uiState.appearanceMode) {
                    1 -> false
                    2 -> true
                    else -> isSystemDark
                }
                val themes = getPreMadeThemes(isDark)
                for (i in themes.indices step 2) {
                    Row(modifier = Modifier.fillMaxWidth()) {
                        Box(modifier = Modifier.weight(1f)) {
                            ThemeCard(
                                theme = themes[i],
                                selected = uiState.currentTheme == themes[i].name,
                                onClick = { viewModel.setTheme(themes[i].name) }
                            )
                        }
                        if (i + 1 < themes.size) {
                            Box(modifier = Modifier.weight(1f)) {
                                ThemeCard(
                                    theme = themes[i + 1],
                                    selected = uiState.currentTheme == themes[i + 1].name,
                                    onClick = { viewModel.setTheme(themes[i + 1].name) }
                                )
                            }
                        } else {
                            Spacer(modifier = Modifier.weight(1f))
                        }
                    }
                }
            }"""

content = content.replace(old_grid, new_grid)

# Remove the import of LazyVerticalGrid, grid.items, etc.
content = content.replace("import androidx.compose.foundation.lazy.grid.GridCells\n", "")
content = content.replace("import androidx.compose.foundation.lazy.grid.LazyVerticalGrid\n", "")
content = content.replace("import androidx.compose.foundation.lazy.grid.items\n", "")

with open('app/src/main/java/com/example/ui/screens/ColorCustomizationScreen.kt', 'w') as f:
    f.write(content)
