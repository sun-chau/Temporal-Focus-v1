package com.example.data

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import kotlinx.coroutines.flow.Flow

@Dao
interface TimerTaskDao {
    @Query("SELECT * FROM timer_tasks ORDER BY targetDateTime ASC")
    fun getAllTasks(): Flow<List<TimerTask>>

    @Query("SELECT * FROM timer_tasks WHERE isCompleted = 0 ORDER BY targetDateTime ASC")
    fun getActiveTasks(): Flow<List<TimerTask>>

    @Query("SELECT * FROM timer_tasks WHERE isCompleted = 1 ORDER BY completedAt DESC")
    fun getCompletedTasks(): Flow<List<TimerTask>>

    @Query("SELECT * FROM timer_tasks WHERE id = :id LIMIT 1")
    fun getTaskByIdSync(id: String): TimerTask?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertTask(task: TimerTask)

    @Update
    suspend fun updateTask(task: TimerTask)

    @Query("DELETE FROM timer_tasks WHERE id = :id")
    suspend fun deleteTaskById(id: String)

    @Query("DELETE FROM timer_tasks WHERE isCompleted = 1")
    suspend fun deleteAllCompletedTasks()

    @Query("DELETE FROM timer_tasks")
    suspend fun deleteAllTasks()
}
