package com.example.ui.components

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.RectangleShape
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.example.data.TimerTask
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@Composable
fun TerminalReminderRow(
    task: TimerTask,
    use24HourFormat: Boolean,
    onComplete: (TimerTask) -> Unit
) {
    var isChecked by remember { mutableStateOf(false) }
    val alpha by animateFloatAsState(targetValue = if (isChecked) 0.3f else 1f)

    val currentTime = System.currentTimeMillis()
    val isOverdue = task.deadlineDateTime != null && task.deadlineDateTime < currentTime
    val isImminent = task.deadlineDateTime != null && task.deadlineDateTime > currentTime && (task.deadlineDateTime - currentTime) <= 86400000L

    val threatColor = when {
        isOverdue -> MaterialTheme.colorScheme.error
        isImminent -> Color(0xFFFFA000) // Amber/Orange
        else -> MaterialTheme.colorScheme.onSurfaceVariant
    }

    val priorityTag = when (task.priority) {
        "CRITICAL" -> "[ CRITICAL ] "
        "MID" -> "[ MID ] "
        "LOW" -> "[ LOW ] "
        else -> ""
    }
    val nameText = "$priorityTag${task.name}".uppercase(Locale.getDefault())

    val timeString = task.deadlineDateTime?.let {
        val format = if (use24HourFormat) "HH:mm MMM d" else "h:mm a MMM d"
        "[ " + SimpleDateFormat(format, Locale.getDefault()).format(Date(it)).uppercase(Locale.getDefault()) + " ]"
    } ?: "[ NO DEADLINE ]"

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .alpha(alpha)
            .border(1.dp, threatColor, RectangleShape)
            .padding(8.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Column(modifier = Modifier.weight(1f).padding(end = 8.dp)) {
            Text(
                text = nameText,
                fontFamily = FontFamily.Monospace,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold,
                color = threatColor
            )
            Spacer(modifier = Modifier.height(2.dp))
            Text(
                text = timeString,
                fontFamily = FontFamily.Monospace,
                style = MaterialTheme.typography.bodySmall,
                color = threatColor
            )
        }
        Text(
            text = if (isChecked) "[ X ]" else "[   ]",
            fontFamily = FontFamily.Monospace,
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.Bold,
            color = threatColor,
            modifier = Modifier.clickable {
                if (!isChecked) {
                    isChecked = true
                    onComplete(task)
                }
            }.padding(4.dp)
        )
    }
}
