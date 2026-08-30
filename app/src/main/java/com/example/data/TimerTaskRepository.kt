package com.example.data

import kotlinx.coroutines.flow.Flow

class TimerTaskRepository(private val dao: TimerTaskDao) {
    val allTasks: Flow<List<TimerTask>> = dao.getAllTasks()
    val activeTasks: Flow<List<TimerTask>> = dao.getActiveTasks()
    val completedTasks: Flow<List<TimerTask>> = dao.getCompletedTasks()

    fun getTaskByIdSync(id: String): TimerTask? = dao.getTaskByIdSync(id)

    suspend fun insertTask(task: TimerTask) {
        dao.insertTask(task)
    }

    suspend fun updateTask(task: TimerTask) {
        dao.updateTask(task)
    }

    suspend fun deleteTaskById(id: String) {
        dao.deleteTaskById(id)
    }

    suspend fun deleteAllCompletedTasks() {
        dao.deleteAllCompletedTasks()
    }

    suspend fun deleteAllTasks() {
        dao.deleteAllTasks()
    }
}
