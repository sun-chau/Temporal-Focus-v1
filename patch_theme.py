import re

with open('app/src/main/java/com/example/ui/theme/Theme.kt', 'r') as f:
    content = f.read()

replacement = """
    val parsedPrimary = baseColorScheme.primary
    val parsedBackground = safeParseColor(customBackdropColor, baseColorScheme.background)
    val parsedOnBackground = safeParseColor(customBaseTextColor, baseColorScheme.onBackground)

    val finalColorScheme = baseColorScheme.copy(
        background = parsedBackground,
        onBackground = parsedOnBackground,
        onSurface = parsedOnBackground,
        error = safeParseColor(customOverdueTextColor, baseColorScheme.error),
        surface = safeParseColor(customBackdropColor, baseColorScheme.surface, 0.9f),
        surfaceVariant = parsedPrimary.copy(alpha = 0.1f),
        onSurfaceVariant = parsedOnBackground.copy(alpha = 0.8f),
        primaryContainer = parsedPrimary.copy(alpha = 0.2f),
        onPrimaryContainer = parsedPrimary,
        secondary = parsedPrimary.copy(alpha = 0.8f),
        secondaryContainer = parsedPrimary.copy(alpha = 0.15f),
        onSecondaryContainer = parsedPrimary,
        tertiary = parsedPrimary.copy(alpha = 0.6f),
        tertiaryContainer = parsedPrimary.copy(alpha = 0.1f),
        onTertiaryContainer = parsedPrimary,
        outline = parsedOnBackground.copy(alpha = 0.2f),
        outlineVariant = parsedOnBackground.copy(alpha = 0.1f)
    )
"""

content = re.sub(
    r'val finalColorScheme = baseColorScheme\.copy\([^)]+\)',
    replacement.strip(),
    content,
    flags=re.MULTILINE|re.DOTALL
)

with open('app/src/main/java/com/example/ui/theme/Theme.kt', 'w') as f:
    f.write(content)
