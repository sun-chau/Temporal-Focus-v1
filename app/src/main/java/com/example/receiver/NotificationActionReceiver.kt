package com.example.receiver

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.util.Log
import androidx.core.app.NotificationManagerCompat
import com.example.data.AppDatabase
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

class NotificationActionReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        val action = intent.action
        val taskId = intent.getStringExtra("TASK_ID") ?: return
        val notificationId = intent.getIntExtra("NOTIFICATION_ID", -1)
        
        Log.d("NotificationAction", "Received action: $action for task: $taskId")
        
        val db = AppDatabase.getDatabase(context)
        val repo = com.example.data.TimerTaskRepository(db.timerTaskDao())
        
        CoroutineScope(Dispatchers.IO).launch {
            if (action == "MARK_COMPLETE") {
                val task = repo.getTaskByIdSync(taskId)
                if (task != null) {
                    repo.updateTask(task.copy(isCompleted = true, completedAt = System.currentTimeMillis()))
                    if (notificationId != -1) {
                        NotificationManagerCompat.from(context).cancel(notificationId)
                    }
                }
            } else if (action == "SNOOZE") {
                if (notificationId != -1) {
                    NotificationManagerCompat.from(context).cancel(notificationId)
                }
                // Snooze logic: in a real app, schedule an alarm for 5 mins later.
            }
        }
    }
}
