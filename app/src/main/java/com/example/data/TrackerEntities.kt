package com.example.data

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.util.UUID

enum class TrackerType { FINITE, ENDLESS }
enum class TrackerUnit { DISCRETE, CONTINUOUS }

@Entity(tableName = "trackers")
data class TrackerEntity(
    @PrimaryKey val id: String = UUID.randomUUID().toString(),
    val title: String = "",
    val type: TrackerType = TrackerType.ENDLESS,
    val unit: TrackerUnit = TrackerUnit.DISCRETE,
    val totalVolume: Float? = null,
    val staticDailyTarget: Float = 1f,
    val deadlineMillis: Long? = null,
    val bankedDays: Int = 0,
    val currentStreak: Int = 0,
    val streakAtRisk: Boolean = false,
    val createdAt: Long = System.currentTimeMillis()
)

@Entity(tableName = "tracker_logs")
data class TrackerLogEntity(
    @PrimaryKey val logId: String = UUID.randomUUID().toString(),
    val trackerId: String,
    val dateString: String, // YYYY-MM-DD
    val loggedVolume: Float
)
