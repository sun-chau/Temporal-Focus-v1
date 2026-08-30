package com.example.data

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import kotlinx.coroutines.flow.Flow

@Dao
interface DailyScheduleDao {
    @Query("SELECT * FROM daily_schedules ORDER BY startTime ASC")
    fun getAllSchedules(): Flow<List<DailyScheduleTask>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertSchedule(schedule: DailyScheduleTask)

    @Update
    suspend fun updateSchedule(schedule: DailyScheduleTask)

    @Delete
    suspend fun deleteSchedule(schedule: DailyScheduleTask)

    @Query("SELECT * FROM daily_schedules WHERE id = :id LIMIT 1")
    fun getScheduleSync(id: String): DailyScheduleTask?

    @Query("SELECT * FROM daily_schedules ORDER BY startTime ASC")
    fun getAllSchedulesSync(): List<DailyScheduleTask>
    
    @Query("DELETE FROM daily_schedules WHERE seriesId = :seriesId")
    suspend fun deleteSeries(seriesId: String)
    
    @Query("UPDATE daily_schedules SET title = :title, label = :label, startTime = startTime + :timeDelta, endTime = endTime + :timeDelta WHERE seriesId = :seriesId")
    suspend fun updateSeries(seriesId: String, title: String, label: String, timeDelta: Long)
    
    @Query("UPDATE daily_schedules SET seriesId = null WHERE id = :id")
    suspend fun breakFromSeries(id: String)
    
    @Update
    suspend fun updateSchedules(schedules: List<DailyScheduleTask>)

}
