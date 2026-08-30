package com.example.ui.theme

import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext

private val DefaultDarkColorScheme = darkColorScheme(
    primary = ObsidianPrimary,
    background = ObsidianBackdrop,
    surface = ObsidianSurface,
    onBackground = ObsidianBaseText,
    onSurface = ObsidianBaseText,
    error = ObsidianOverdueText
)

private val DefaultLightColorScheme = lightColorScheme(
    primary = DaylightPrimary,
    background = DaylightBackdrop,
    surface = DaylightSurface,
    onBackground = DaylightBaseText,
    onSurface = DaylightBaseText,
    error = DaylightOverdueText
)

private val MidnightDarkColorScheme = darkColorScheme(
    primary = MidnightDarkPrimary,
    background = MidnightDarkBackdrop,
    surface = MidnightDarkSurface,
    onBackground = MidnightDarkBaseText,
    onSurface = MidnightDarkBaseText,
    error = MidnightDarkOverdueText
)

private val MidnightLightColorScheme = lightColorScheme(
    primary = MidnightLightPrimary,
    background = MidnightLightBackdrop,
    surface = MidnightLightSurface,
    onBackground = MidnightLightBaseText,
    onSurface = MidnightLightBaseText,
    error = MidnightLightOverdueText
)

private val AmberDarkColorScheme = darkColorScheme(
    primary = AmberDarkPrimary,
    background = AmberDarkBackdrop,
    surface = AmberDarkSurface,
    onBackground = AmberDarkBaseText,
    onSurface = AmberDarkBaseText,
    error = AmberDarkOverdueText
)

private val AmberLightColorScheme = lightColorScheme(
    primary = AmberLightPrimary,
    background = AmberLightBackdrop,
    surface = AmberLightSurface,
    onBackground = AmberLightBaseText,
    onSurface = AmberLightBaseText,
    error = AmberLightOverdueText
)

private val NordicDarkColorScheme = darkColorScheme(
    primary = NordicDarkPrimary,
    background = NordicDarkBackdrop,
    surface = NordicDarkSurface,
    onBackground = NordicDarkBaseText,
    onSurface = NordicDarkBaseText,
    error = NordicDarkOverdueText
)

private val NordicLightColorScheme = lightColorScheme(
    primary = NordicLightPrimary,
    background = NordicLightBackdrop,
    surface = NordicLightSurface,
    onBackground = NordicLightBaseText,
    onSurface = NordicLightBaseText,
    error = NordicLightOverdueText
)

private val ForestDarkColorScheme = darkColorScheme(
    primary = ForestDarkPrimary,
    background = ForestDarkBackdrop,
    surface = ForestDarkSurface,
    onBackground = ForestDarkBaseText,
    onSurface = ForestDarkBaseText,
    error = ForestDarkOverdueText
)

private val ForestLightColorScheme = lightColorScheme(
    primary = ForestLightPrimary,
    background = ForestLightBackdrop,
    surface = ForestLightSurface,
    onBackground = ForestLightBaseText,
    onSurface = ForestLightBaseText,
    error = ForestLightOverdueText
)

private val CrimsonDarkColorScheme = darkColorScheme(
    primary = CrimsonDarkPrimary,
    background = CrimsonDarkBackdrop,
    surface = CrimsonDarkSurface,
    onBackground = CrimsonDarkBaseText,
    onSurface = CrimsonDarkBaseText,
    error = CrimsonDarkOverdueText
)

private val CrimsonLightColorScheme = lightColorScheme(
    primary = CrimsonLightPrimary,
    background = CrimsonLightBackdrop,
    surface = CrimsonLightSurface,
    onBackground = CrimsonLightBaseText,
    onSurface = CrimsonLightBaseText,
    error = CrimsonLightOverdueText
)

private val MonochromeDarkColorScheme = darkColorScheme(
    primary = MonochromeDarkPrimary,
    background = MonochromeDarkBackdrop,
    surface = MonochromeDarkSurface,
    onBackground = MonochromeDarkBaseText,
    onSurface = MonochromeDarkBaseText,
    error = MonochromeDarkOverdueText
)

private val MonochromeLightColorScheme = lightColorScheme(
    primary = MonochromeLightPrimary,
    background = MonochromeLightBackdrop,
    surface = MonochromeLightSurface,
    onBackground = MonochromeLightBaseText,
    onSurface = MonochromeLightBaseText,
    error = MonochromeLightOverdueText
)

@Composable
fun MyApplicationTheme(
    themeName: String = "Default",
    appearanceMode: Int = 0,
    customBackdropColor: String = "",
    customBaseTextColor: String = "",
    customOverdueTextColor: String = "",
    content: @Composable () -> Unit,
) {
    val isSystemDark = isSystemInDarkTheme()
    val isDark = when (appearanceMode) {
        1 -> false
        2 -> true
        else -> isSystemDark
    }

    val baseColorScheme = if (isDark) {
        when (themeName) {
            "Midnight Minimalist" -> MidnightDarkColorScheme
            "Amber Glow" -> AmberDarkColorScheme
            "Nordic Frost" -> NordicDarkColorScheme
            "Forest Canopy" -> ForestDarkColorScheme
            "Crimson Twilight" -> CrimsonDarkColorScheme
            "Monochrome" -> MonochromeDarkColorScheme
            else -> DefaultDarkColorScheme
        }
    } else {
        when (themeName) {
            "Midnight Minimalist" -> MidnightLightColorScheme
            "Amber Glow" -> AmberLightColorScheme
            "Nordic Frost" -> NordicLightColorScheme
            "Forest Canopy" -> ForestLightColorScheme
            "Crimson Twilight" -> CrimsonLightColorScheme
            "Monochrome" -> MonochromeLightColorScheme
            else -> DefaultLightColorScheme
        }
    }
    
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

    MaterialTheme(colorScheme = finalColorScheme, typography = Typography, content = content)
}

fun safeParseColor(colorString: String, defaultColor: androidx.compose.ui.graphics.Color, alpha: Float = 1.0f): androidx.compose.ui.graphics.Color {
    if (colorString.isEmpty()) return defaultColor
    return try {
        androidx.compose.ui.graphics.Color(android.graphics.Color.parseColor(colorString)).copy(alpha = alpha)
    } catch (e: Exception) {
        defaultColor
    }
}
