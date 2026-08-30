import re

with open('app/src/main/java/com/example/ui/theme/Color.kt', 'w') as f:
    f.write("""package com.example.ui.theme

import androidx.compose.ui.graphics.Color

// Default Theme (Obsidian Dark / Daylight Clear)
val ObsidianBackdrop = Color(0xFF000000)
val ObsidianSurface = Color(0xFF1C1C1E)
val ObsidianBaseText = Color(0xFFE5E5EA)
val ObsidianOverdueText = Color(0xFFFF453A)
val ObsidianPrimary = Color(0xFF0A84FF)

val DaylightBackdrop = Color(0xFFF9FAFB)
val DaylightSurface = Color(0xFFFFFFFF)
val DaylightBaseText = Color(0xFF111827)
val DaylightOverdueText = Color(0xFFEF4444)
val DaylightPrimary = Color(0xFF3B82F6)

// Midnight Minimalist
val MidnightDarkBackdrop = Color(0xFF09090B)
val MidnightDarkSurface = Color(0xFF18181B)
val MidnightDarkBaseText = Color(0xFFF4F4F5)
val MidnightDarkOverdueText = Color(0xFFF43F5E)
val MidnightDarkPrimary = Color(0xFFFF8C00)

val MidnightLightBackdrop = Color(0xFFFAFAFA)
val MidnightLightSurface = Color(0xFFFFFFFF)
val MidnightLightBaseText = Color(0xFF09090B)
val MidnightLightOverdueText = Color(0xFFE11D48)
val MidnightLightPrimary = Color(0xFFEA580C)

// Amber Glow
val AmberDarkBackdrop = Color(0xFF1C0D02)
val AmberDarkSurface = Color(0xFF2C1A09)
val AmberDarkBaseText = Color(0xFFFCD34D)
val AmberDarkOverdueText = Color(0xFFF59E0B)
val AmberDarkPrimary = Color(0xFFF59E0B)

val AmberLightBackdrop = Color(0xFFFFFBEB)
val AmberLightSurface = Color(0xFFFEF3C7)
val AmberLightBaseText = Color(0xFF78350F)
val AmberLightOverdueText = Color(0xFFD97706)
val AmberLightPrimary = Color(0xFFD97706)

// Nordic Frost
val NordicDarkBackdrop = Color(0xFF0F172A)
val NordicDarkSurface = Color(0xFF1E293B)
val NordicDarkBaseText = Color(0xFFE2E8F0)
val NordicDarkOverdueText = Color(0xFFF97316)
val NordicDarkPrimary = Color(0xFF38BDF8)

val NordicLightBackdrop = Color(0xFFF0F9FF)
val NordicLightSurface = Color(0xFFE0F2FE)
val NordicLightBaseText = Color(0xFF0F172A)
val NordicLightOverdueText = Color(0xFFEA580C)
val NordicLightPrimary = Color(0xFF0284C7)

// Forest Canopy
val ForestDarkBackdrop = Color(0xFF06402B)
val ForestDarkSurface = Color(0xFF0D5D42)
val ForestDarkBaseText = Color(0xFFD1FAE5)
val ForestDarkOverdueText = Color(0xFFFCD34D)
val ForestDarkPrimary = Color(0xFF10B981)

val ForestLightBackdrop = Color(0xFFECFDF5)
val ForestLightSurface = Color(0xFFD1FAE5)
val ForestLightBaseText = Color(0xFF064E3B)
val ForestLightOverdueText = Color(0xFFD97706)
val ForestLightPrimary = Color(0xFF059669)

// Crimson Twilight
val CrimsonDarkBackdrop = Color(0xFF2A0A18)
val CrimsonDarkSurface = Color(0xFF4A152C)
val CrimsonDarkBaseText = Color(0xFFFCE7F3)
val CrimsonDarkOverdueText = Color(0xFFF43F5E)
val CrimsonDarkPrimary = Color(0xFFE11D48)

val CrimsonLightBackdrop = Color(0xFFFFF1F2)
val CrimsonLightSurface = Color(0xFFFFE4E6)
val CrimsonLightBaseText = Color(0xFF881337)
val CrimsonLightOverdueText = Color(0xFFE11D48)
val CrimsonLightPrimary = Color(0xFFBE123C)

// Monochrome
val MonochromeDarkBackdrop = Color(0xFF121212)
val MonochromeDarkSurface = Color(0xFF242424)
val MonochromeDarkBaseText = Color(0xFFFFFFFF)
val MonochromeDarkOverdueText = Color(0xFF9E9E9E)
val MonochromeDarkPrimary = Color(0xFFE0E0E0)

val MonochromeLightBackdrop = Color(0xFFF5F5F5)
val MonochromeLightSurface = Color(0xFFFFFFFF)
val MonochromeLightBaseText = Color(0xFF000000)
val MonochromeLightOverdueText = Color(0xFF757575)
val MonochromeLightPrimary = Color(0xFF424242)
""")

with open('app/src/main/java/com/example/ui/theme/Theme.kt', 'w') as f:
    f.write("""package com.example.ui.theme

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
    
    val finalColorScheme = baseColorScheme.copy(
        background = if (customBackdropColor.isNotEmpty()) androidx.compose.ui.graphics.Color(android.graphics.Color.parseColor(customBackdropColor)) else baseColorScheme.background,
        onBackground = if (customBaseTextColor.isNotEmpty()) androidx.compose.ui.graphics.Color(android.graphics.Color.parseColor(customBaseTextColor)) else baseColorScheme.onBackground,
        onSurface = if (customBaseTextColor.isNotEmpty()) androidx.compose.ui.graphics.Color(android.graphics.Color.parseColor(customBaseTextColor)) else baseColorScheme.onSurface,
        error = if (customOverdueTextColor.isNotEmpty()) androidx.compose.ui.graphics.Color(android.graphics.Color.parseColor(customOverdueTextColor)) else baseColorScheme.error,
        surface = if (customBackdropColor.isNotEmpty()) androidx.compose.ui.graphics.Color(android.graphics.Color.parseColor(customBackdropColor)).copy(alpha = 0.9f) else baseColorScheme.surface
    )

    MaterialTheme(colorScheme = finalColorScheme, typography = Typography, content = content)
}
""")

