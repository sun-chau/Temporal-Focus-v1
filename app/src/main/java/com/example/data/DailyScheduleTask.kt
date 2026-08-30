package com.example.data

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.util.UUID

enum class ScheduleStatus {
    NOT_DONE, COMPLETED, SKIPPED, DROPPED
}

@Entity(tableName = "daily_schedules")
data class DailyScheduleTask(
    @PrimaryKey val id: String = UUID.randomUUID().toString(),
    val title: String,
    val startTime: Long,
    val endTime: Long,
    val label: String = "",
    val status: String = ScheduleStatus.NOT_DONE.name,
    val laneIndex: Int = 0,
    val isFinished: Boolean = false,
    val seriesId: String? = null,
    val recurrenceType: String? = null,
    val seriesEndDate: Long? = null
)
