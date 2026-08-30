package com.example.data

import java.util.Calendar

object MockDataGenerator {
    fun getMockTasks(): List<DailyScheduleTask> {
        val todayStart = getStartOfDayMillis(System.currentTimeMillis())
        
        return listOf(
            DailyScheduleTask(
                title = "Morning Sync",
                startTime = todayStart + 9 * 3600000L, // 09:00
                endTime = todayStart + 10 * 3600000L + 1800000L, // 10:30
                label = "Work",
                laneIndex = 0
            ),
            DailyScheduleTask(
                title = "Deep Work",
                startTime = todayStart + 10 * 3600000L, // 10:00 (overlaps Morning Sync)
                endTime = todayStart + 11 * 3600000L + 1800000L, // 11:30
                label = "Focus",
                laneIndex = 1
            ),
            DailyScheduleTask(
                title = "Quick Call",
                startTime = todayStart + 10 * 3600000L + 900000L, // 10:15 (overlaps both)
                endTime = todayStart + 11 * 3600000L, // 11:00
                label = "Meeting",
                laneIndex = 2
            ),
            DailyScheduleTask(
                title = "Lunch",
                startTime = todayStart + 12 * 3600000L, // 12:00
                endTime = todayStart + 13 * 3600000L, // 13:00
                label = "Personal",
                laneIndex = 0
            ),
            DailyScheduleTask(
                title = "Project Review",
                startTime = todayStart + 14 * 3600000L, // 14:00
                endTime = todayStart + 15 * 3600000L, // 15:00
                label = "Work",
                laneIndex = 0
            ),
            DailyScheduleTask(
                title = "Overnight Processing",
                startTime = todayStart + 22 * 3600000L, // 22:00
                endTime = todayStart + 24 * 3600000L + 6 * 3600000L, // 06:00 next day (Multi-day)
                label = "System",
                laneIndex = 0
            ),
            DailyScheduleTask(
                title = "Morning Workout",
                startTime = todayStart + 24 * 3600000L + 7 * 3600000L, // 07:00 tomorrow
                endTime = todayStart + 24 * 3600000L + 8 * 3600000L, // 08:00 tomorrow
                label = "Health",
                laneIndex = 0
            )
        )
    }

    private fun getStartOfDayMillis(timeInMillis: Long): Long {
        val cal = Calendar.getInstance().apply {
            this.timeInMillis = timeInMillis
            set(Calendar.HOUR_OF_DAY, 0)
            set(Calendar.MINUTE, 0)
            set(Calendar.SECOND, 0)
            set(Calendar.MILLISECOND, 0)
        }
        return cal.timeInMillis
    }
}
