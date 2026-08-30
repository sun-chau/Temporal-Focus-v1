package com.example.ui.utils

import androidx.compose.ui.graphics.Color
import kotlin.math.absoluteValue

fun getLabelColor(label: String, isEnabled: Boolean): Color {
    if (!isEnabled || label.isBlank()) return Color.Transparent
    val parts = label.split("|", limit = 2)
    val colorStr = parts.getOrNull(1)
    if (colorStr != null) {
        try {
            val colorInt = android.graphics.Color.parseColor(colorStr)
            return Color(colorInt)
        } catch (e: Exception) {
            // fallback to random
        }
    }
    
    // Generate stable random color based on string hash
    val hash = parts[0].trim().hashCode().absoluteValue
    val r = (hash and 0xFF0000 shr 16) % 128 + 127 // Keep it bright
    val g = (hash and 0x00FF00 shr 8) % 128 + 127
    val b = (hash and 0x0000FF) % 128 + 127
    return Color(r, g, b, 255)
}

fun getLabelName(label: String): String {
    return label.split("|", limit = 2)[0].trim()
}
