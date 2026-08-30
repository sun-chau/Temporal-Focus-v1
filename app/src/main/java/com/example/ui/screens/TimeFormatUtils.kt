package com.example.ui.screens

import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

object TimeFormatUtils {
    fun formatDateTime(timeMillis: Long, use24HourFormat: Boolean, includeSeconds: Boolean = false): String {
        val pattern = if (use24HourFormat) {
            if (includeSeconds) "MMM dd, yyyy HH:mm:ss" else "MMM dd, yyyy HH:mm"
        } else {
            if (includeSeconds) "MMM dd, yyyy hh:mm:ss a" else "MMM dd, yyyy hh:mm a"
        }
        return SimpleDateFormat(pattern, Locale.getDefault()).format(Date(timeMillis))
    }

    fun formatTimeOnly(timeMillis: Long, use24HourFormat: Boolean, includeSeconds: Boolean = false): String {
        val pattern = if (use24HourFormat) {
            if (includeSeconds) "HH:mm:ss" else "HH:mm"
        } else {
            if (includeSeconds) "hh:mm:ss a" else "hh:mm a"
        }
        return SimpleDateFormat(pattern, Locale.getDefault()).format(Date(timeMillis))
    }

    fun formatDayTime(timeMillis: Long, use24HourFormat: Boolean): String {
        val pattern = if (use24HourFormat) "MMM d, HH:mm" else "MMM d, hh:mm a"
        return SimpleDateFormat(pattern, Locale.getDefault()).format(Date(timeMillis))
    }

    fun formatFullWithDay(timeMillis: Long, use24HourFormat: Boolean): String {
        val pattern = if (use24HourFormat) "EEEE, MMM d, yyyy • HH:mm" else "EEEE, MMM d, yyyy • h:mm a"
        return SimpleDateFormat(pattern, Locale.getDefault()).format(Date(timeMillis))
    }
}
