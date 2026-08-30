package com.example.data

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import kotlinx.coroutines.flow.Flow

@Dao
interface TrackerDao {
    @Query("SELECT * FROM trackers ORDER BY createdAt DESC")
    fun getAllTrackers(): Flow<List<TrackerEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertTracker(tracker: TrackerEntity)

    @Update
    suspend fun updateTracker(tracker: TrackerEntity)

    @Delete
    suspend fun deleteTracker(tracker: TrackerEntity)

    @Query("SELECT * FROM tracker_logs WHERE trackerId = :trackerId ORDER BY dateString DESC")
    fun getLogsForTracker(trackerId: String): Flow<List<TrackerLogEntity>>
    
    @Query("SELECT * FROM tracker_logs")
    fun getAllLogs(): Flow<List<TrackerLogEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertLog(log: TrackerLogEntity)

    @Delete
    suspend fun deleteLog(log: TrackerLogEntity)
    
    @Query("SELECT * FROM tracker_logs WHERE trackerId = :trackerId AND dateString = :dateString LIMIT 1")
    suspend fun getLogForDate(trackerId: String, dateString: String): TrackerLogEntity?
}
