package com.example.data

import androidx.room.Entity
import androidx.room.PrimaryKey
import com.squareup.moshi.JsonClass
import java.util.UUID

enum class RecurrenceType {
    NONE, DAILY, WEEKLY, MONTHLY, ANNUALLY, CUSTOM, SPECIFIC_WEEKDAYS, SPECIFIC_DATES
}

@JsonClass(generateAdapter = true)
@Entity(tableName = "timer_tasks")
data class TimerTask(
    @PrimaryKey val id: String = UUID.randomUUID().toString(),
    val name: String,
    val description: String? = null,
    val labels: String = "",
    val createdAt: Long = System.currentTimeMillis(),
    val targetDateTime: Long,
    val completedAt: Long? = null,
    val isCompleted: Boolean = false,
    val isPinned: Boolean = false,
    
    val recurrenceType: String = RecurrenceType.NONE.name,
    val customDaysInterval: Int? = null,
    val maxRepetitions: Int? = null,
    val completionCount: Int = 0,
    val specificDays: String? = null,
    
    val recurring: String? = null,
    val completionStatus: String? = null,
    val shiftedAmount: Long = 0L,
    val priority: String = "Normal",
    val deadlineDateTime: Long? = null,
    val link: String? = null,
    val attachmentUri: String? = null
)
