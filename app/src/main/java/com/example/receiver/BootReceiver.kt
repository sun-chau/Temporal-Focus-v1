package com.example.receiver

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import com.example.data.AppDatabase
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch

class BootReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == Intent.ACTION_BOOT_COMPLETED) {
            val db = AppDatabase.getDatabase(context)
            val repo = com.example.data.TimerTaskRepository(db.timerTaskDao())
            
            CoroutineScope(Dispatchers.IO).launch {
                // In a real app we'd fetch appSettings to get the offset, but here we can just use 15 mins default
                // or read it from DataStore. Let's assume 15 mins for now, or fetch active tasks and reschedule.
                val activeTasks = repo.activeTasks.first()
                for (task in activeTasks) {
                    AlarmScheduler.scheduleAlarmsForTask(context, task, 15) // hardcoding 15 as fallback, ideally read from settings
                }
            }
        }
    }
}
