package com.example.util

import java.util.Calendar

data class ParsedCommand(val cleanTitle: String, val epochMillis: Long?, val priority: String)

fun parseTerminalCommand(input: String): ParsedCommand {
    var cleanTitle = input
    var priority = "Normal"
    var epochMillis: Long? = null

    // Priority Regex
    val priorityRegex = Regex("(?i)!(high|mid|low)\\b")
    val priorityMatch = priorityRegex.find(cleanTitle)
    if (priorityMatch != null) {
        priority = when (priorityMatch.groupValues[1].lowercase()) {
            "high" -> "CRITICAL"
            "mid" -> "MID"
            "low" -> "LOW"
            else -> "Normal"
        }
        cleanTitle = cleanTitle.replace(priorityMatch.value, "")
    }

    // Time Regex (@)
    val timeRegex = Regex("(?i)@\\s*(tmrw|tomorrow|today)?\\s*(?:(\\d{1,2}):(\\d{2})|(\\d{1,2})\\s*([ap]m))?\\s*(tmrw|tomorrow|today)?")
    val timeMatch = timeRegex.find(cleanTitle)
    
    if (timeMatch != null && timeMatch.value.trim() != "@") {
        val g1 = timeMatch.groupValues[1].lowercase()
        val g2 = timeMatch.groupValues[2] // HH
        val g3 = timeMatch.groupValues[3] // mm
        val g4 = timeMatch.groupValues[4] // H (am/pm)
        val g5 = timeMatch.groupValues[5].lowercase() // am/pm
        val g6 = timeMatch.groupValues[6].lowercase()
        
        val dayOffset = if (g1 == "tmrw" || g1 == "tomorrow" || g6 == "tmrw" || g6 == "tomorrow") 1 else 0
        
        val cal = Calendar.getInstance()
        cal.add(Calendar.DAY_OF_YEAR, dayOffset)
        
        var timeSet = false
        if (g2.isNotEmpty() && g3.isNotEmpty()) {
            cal.set(Calendar.HOUR_OF_DAY, g2.toInt())
            cal.set(Calendar.MINUTE, g3.toInt())
            timeSet = true
        } else if (g4.isNotEmpty() && g5.isNotEmpty()) {
            var h = g4.toInt()
            if (g5 == "pm" && h < 12) h += 12
            if (g5 == "am" && h == 12) h = 0
            cal.set(Calendar.HOUR_OF_DAY, h)
            cal.set(Calendar.MINUTE, 0)
            timeSet = true
        }
        
        if (timeSet || dayOffset > 0 || g1 == "today" || g6 == "today") {
            if (timeSet) {
                cal.set(Calendar.SECOND, 0)
                cal.set(Calendar.MILLISECOND, 0)
            }
            epochMillis = cal.timeInMillis
            cleanTitle = cleanTitle.replace(timeMatch.value, "")
        }
    }

    return ParsedCommand(
        cleanTitle = cleanTitle.trim().replace(Regex("\\s+"), " "),
        epochMillis = epochMillis,
        priority = priority
    )
}
