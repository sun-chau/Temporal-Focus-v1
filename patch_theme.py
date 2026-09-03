import re

with open('app/src/main/java/com/example/ui/theme/Theme.kt', 'r') as f:
    content = f.read()

if 'import androidx.compose.ui.graphics.compositeOver' not in content:
    content = content.replace('import androidx.compose.material3.MaterialTheme', 'import androidx.compose.material3.MaterialTheme\nimport androidx.compose.ui.graphics.compositeOver')

replacement = """
    val parsedPrimary = baseColorScheme.primary
    val parsedBackground = safeParseColor(customBackdropColor, baseColorScheme.background)
    val parsedOnBackground = safeParseColor(customBaseTextColor, baseColorScheme.onBackground)

    val finalColorScheme = baseColorScheme.copy(
        background = parsedBackground,
        onBackground = parsedOnBackground,
        onSurface = parsedOnBackground,
        error = safeParseColor(customOverdueTextColor, baseColorScheme.error),
        surface = safeParseColor(customBackdropColor, baseColorScheme.surface, 1.0f).compositeOver(parsedBackground),
        surfaceVariant = parsedPrimary.copy(alpha = 0.1f).compositeOver(parsedBackground),
        onSurfaceVariant = parsedOnBackground.copy(alpha = 0.8f).compositeOver(parsedBackground),
        primaryContainer = parsedPrimary.copy(alpha = 0.2f).compositeOver(parsedBackground),
        onPrimaryContainer = parsedPrimary,
        secondary = parsedPrimary.copy(alpha = 0.8f).compositeOver(parsedBackground),
        secondaryContainer = parsedPrimary.copy(alpha = 0.15f).compositeOver(parsedBackground),
        onSecondaryContainer = parsedPrimary,
        tertiary = parsedPrimary.copy(alpha = 0.6f).compositeOver(parsedBackground),
        tertiaryContainer = parsedPrimary.copy(alpha = 0.1f).compositeOver(parsedBackground),
        onTertiaryContainer = parsedPrimary,
        outline = parsedOnBackground.copy(alpha = 0.2f).compositeOver(parsedBackground),
        outlineVariant = parsedOnBackground.copy(alpha = 0.1f).compositeOver(parsedBackground)
    )
"""

content = re.sub(
    r'val parsedPrimary = baseColorScheme\.primary.*?val finalColorScheme = baseColorScheme\.copy\([^)]+\)',
    replacement.strip(),
    content,
    flags=re.MULTILINE|re.DOTALL
)

with open('app/src/main/java/com/example/ui/theme/Theme.kt', 'w') as f:
    f.write(content)
