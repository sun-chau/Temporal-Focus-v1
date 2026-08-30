package com.example.data

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface FocusSessionStatsDao {
    @Query("SELECT * FROM focus_session_stats ORDER BY timestamp DESC")
    fun getAllStats(): Flow<List<FocusSessionStats>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertStat(stat: FocusSessionStats)

    @Query("DELETE FROM focus_session_stats")
    suspend fun deleteAllStats()
}
