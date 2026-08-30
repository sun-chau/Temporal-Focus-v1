import re

with open('app/src/main/java/com/example/ui/screens/ColorCustomizationScreen.kt', 'r') as f:
    content = f.read()

# Replace the hardcoded list with a function that takes isDark
new_themes_func = """
fun getPreMadeThemes(isDark: Boolean): List<ThemeInfo> {
    return if (isDark) {
        listOf(
            ThemeInfo("Default", Color(0xFF0A84FF), Color(0xFF1C1C1E), Color(0xFF000000)),
            ThemeInfo("Midnight Minimalist", Color(0xFFFF8C00), Color(0xFF18181B), Color(0xFF09090B)),
            ThemeInfo("Amber Glow", Color(0xFFF59E0B), Color(0xFF2C1A09), Color(0xFF1C0D02)),
            ThemeInfo("Nordic Frost", Color(0xFF38BDF8), Color(0xFF1E293B), Color(0xFF0F172A)),
            ThemeInfo("Forest Canopy", Color(0xFF10B981), Color(0xFF0D5D42), Color(0xFF06402B)),
            ThemeInfo("Crimson Twilight", Color(0xFFE11D48), Color(0xFF4A152C), Color(0xFF2A0A18)),
            ThemeInfo("Monochrome", Color(0xFFE0E0E0), Color(0xFF242424), Color(0xFF121212))
        )
    } else {
        listOf(
            ThemeInfo("Default", Color(0xFF3B82F6), Color(0xFFFFFFFF), Color(0xFFF9FAFB)),
            ThemeInfo("Midnight Minimalist", Color(0xFFEA580C), Color(0xFFFFFFFF), Color(0xFFFAFAFA)),
            ThemeInfo("Amber Glow", Color(0xFFD97706), Color(0xFFFEF3C7), Color(0xFFFFFBEB)),
            ThemeInfo("Nordic Frost", Color(0xFF0284C7), Color(0xFFE0F2FE), Color(0xFFF0F9FF)),
            ThemeInfo("Forest Canopy", Color(0xFF059669), Color(0xFFD1FAE5), Color(0xFFECFDF5)),
            ThemeInfo("Crimson Twilight", Color(0xFFBE123C), Color(0xFFFFE4E6), Color(0xFFFFF1F2)),
            ThemeInfo("Monochrome", Color(0xFF424242), Color(0xFFFFFFFF), Color(0xFFF5F5F5))
        )
    }
}
"""

# Find the old preMadeThemes declaration
old_themes = """val preMadeThemes = listOf(
    ThemeInfo("Default", Color(0xFF0A84FF), Color(0xFF1C1C1E), Color(0xFF000000)),
    ThemeInfo("Midnight Minimalist", Color(0xFFFF8C00), Color(0xFF18181B), Color(0xFF09090B)),
    ThemeInfo("Amber Glow", Color(0xFFF59E0B), Color(0xFF2C1A09), Color(0xFF1C0D02)),
    ThemeInfo("Nordic Frost", Color(0xFF38BDF8), Color(0xFF1E293B), Color(0xFF0F172A)),
    ThemeInfo("Forest Canopy", Color(0xFF10B981), Color(0xFF0D5D42), Color(0xFF06402B)),
    ThemeInfo("Crimson Twilight", Color(0xFFE11D48), Color(0xFF4A152C), Color(0xFF2A0A18)),
    ThemeInfo("Monochrome", Color(0xFFE0E0E0), Color(0xFF242424), Color(0xFF121212))
)"""

content = content.replace(old_themes, new_themes_func)

# Replace the usage of preMadeThemes inside the Composable
# First, add the isDark logic
composable_start = """fun ColorCustomizationBottomSheet(
    viewModel: MainViewModel,
    uiState: UiState,
    onDismiss: () -> Unit
) {"""

composable_start_with_isdark = """import androidx.compose.foundation.isSystemInDarkTheme\n\n""" + composable_start

if "import androidx.compose.foundation.isSystemInDarkTheme" not in content:
    content = content.replace(composable_start, composable_start_with_isdark)

# Inside the composable:
usage_find = "items(preMadeThemes) { theme ->"

usage_replace = """val isSystemDark = androidx.compose.foundation.isSystemInDarkTheme()
            val isDark = when (uiState.appearanceMode) {
                1 -> false
                2 -> true
                else -> isSystemDark
            }
            items(getPreMadeThemes(isDark)) { theme ->"""

content = content.replace(usage_find, usage_replace)

with open('app/src/main/java/com/example/ui/screens/ColorCustomizationScreen.kt', 'w') as f:
    f.write(content)
