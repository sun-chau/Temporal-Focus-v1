import re

with open('app/src/main/java/com/example/ui/theme/Theme.kt', 'r') as f:
    content = f.read()

new_content = content.replace(
    "background = if (customBackdropColor.isNotEmpty()) androidx.compose.ui.graphics.Color(android.graphics.Color.parseColor(customBackdropColor)) else baseColorScheme.background,",
    "background = safeParseColor(customBackdropColor, baseColorScheme.background),"
).replace(
    "onBackground = if (customBaseTextColor.isNotEmpty()) androidx.compose.ui.graphics.Color(android.graphics.Color.parseColor(customBaseTextColor)) else baseColorScheme.onBackground,",
    "onBackground = safeParseColor(customBaseTextColor, baseColorScheme.onBackground),"
).replace(
    "onSurface = if (customBaseTextColor.isNotEmpty()) androidx.compose.ui.graphics.Color(android.graphics.Color.parseColor(customBaseTextColor)) else baseColorScheme.onSurface,",
    "onSurface = safeParseColor(customBaseTextColor, baseColorScheme.onSurface),"
).replace(
    "error = if (customOverdueTextColor.isNotEmpty()) androidx.compose.ui.graphics.Color(android.graphics.Color.parseColor(customOverdueTextColor)) else baseColorScheme.error,",
    "error = safeParseColor(customOverdueTextColor, baseColorScheme.error),"
).replace(
    "surface = if (customBackdropColor.isNotEmpty()) androidx.compose.ui.graphics.Color(android.graphics.Color.parseColor(customBackdropColor)).copy(alpha = 0.9f) else baseColorScheme.surface",
    "surface = safeParseColor(customBackdropColor, baseColorScheme.surface, 0.9f)"
)

# Add safeParseColor function
safe_parse_func = """
fun safeParseColor(colorString: String, defaultColor: androidx.compose.ui.graphics.Color, alpha: Float = 1.0f): androidx.compose.ui.graphics.Color {
    if (colorString.isEmpty()) return defaultColor
    return try {
        androidx.compose.ui.graphics.Color(android.graphics.Color.parseColor(colorString)).copy(alpha = alpha)
    } catch (e: Exception) {
        defaultColor
    }
}
"""
new_content += safe_parse_func

with open('app/src/main/java/com/example/ui/theme/Theme.kt', 'w') as f:
    f.write(new_content)
