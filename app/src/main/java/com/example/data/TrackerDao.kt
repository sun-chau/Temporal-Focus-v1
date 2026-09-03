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

    @Query("SELECT * FROM trackers WHERE id = :id")
    fun getTrackerById(id: String): Flow<TrackerEntity?>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertTracker(tracker: TrackerEntity)

    @Update
    suspend fun updateTracker(tracker: TrackerEntity)

    @Delete
    suspend fun deleteTracker(tracker: TrackerEntity)
}
