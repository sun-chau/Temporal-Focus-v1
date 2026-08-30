package com.example.data

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.util.UUID

@Entity(tableName = "focus_session_stats")
data class FocusSessionStats(
    @PrimaryKey val id: String = UUID.randomUUID().toString(),
    val timestamp: Long = System.currentTimeMillis(),
    val durationSeconds: Long = 0L,
    val isFocus: Boolean = true,
    val tasksCompletedCount: Int = 0,
    val type: String = "POMODORO" // POMODORO, CHRONOMETER, POMODORO_BREAK
)
