package com.example.receiver

import android.app.AlarmManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.os.Build
import android.util.Log
import com.example.data.TimerTask

object AlarmScheduler {
    fun scheduleAlarmsForTask(context: Context, task: TimerTask, offsetMinutes: Int) {
        val alarmManager = context.getSystemService(Context.ALARM_SERVICE) as AlarmManager
        
        // Exact alarms permission check for Android 12+
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            if (!alarmManager.canScheduleExactAlarms()) {
                Log.w("AlarmScheduler", "Cannot schedule exact alarms, permission missing.")
                return
            }
        }
        
        // Cancel existing alarms first
        cancelAlarmsForTask(context, task.id)
        
        if (task.isCompleted) return
        
        val currentTime = System.currentTimeMillis()
        
        // 1. Schedule "Target Reached" alarm
        if (task.targetDateTime > currentTime) {
            val reachedIntent = Intent(context, TimerAlarmReceiver::class.java).apply {
                putExtra("TASK_ID", task.id)
                putExtra("IS_APPROACHING", false)
            }
            val pendingReached = PendingIntent.getBroadcast(
                context, task.id.hashCode(), reachedIntent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
            
            try {
                alarmManager.setExactAndAllowWhileIdle(
                    AlarmManager.RTC_WAKEUP,
                    task.targetDateTime,
                    pendingReached
                )
            } catch (e: SecurityException) {
                e.printStackTrace()
            }
        }
        
        // 2. Schedule "Approaching" alarm
        val offsetMillis = offsetMinutes * 60 * 1000L
        val approachTime = task.targetDateTime - offsetMillis
        if (offsetMinutes > 0 && approachTime > currentTime) {
            val approachingIntent = Intent(context, TimerAlarmReceiver::class.java).apply {
                putExtra("TASK_ID", task.id)
                putExtra("IS_APPROACHING", true)
                putExtra("OFFSET_MINUTES", offsetMinutes)
            }
            // Use a different request code to distinguish from the reached alarm
            val approachingRequestCode = (task.id + "_approaching").hashCode()
            val pendingApproaching = PendingIntent.getBroadcast(
                context, approachingRequestCode, approachingIntent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
            
            try {
                alarmManager.setExactAndAllowWhileIdle(
                    AlarmManager.RTC_WAKEUP,
                    approachTime,
                    pendingApproaching
                )
            } catch (e: SecurityException) {
                e.printStackTrace()
            }
        }

        // 3. Schedule "Custom Deadline" alarm
        if (task.deadlineDateTime != null && task.deadlineDateTime > currentTime) {
            val deadlineIntent = Intent(context, TimerAlarmReceiver::class.java).apply {
                putExtra("TASK_ID", task.id)
                putExtra("IS_DEADLINE", true)
            }
            val deadlineRequestCode = (task.id + "_deadline").hashCode()
            val pendingDeadline = PendingIntent.getBroadcast(
                context, deadlineRequestCode, deadlineIntent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
            
            try {
                alarmManager.setExactAndAllowWhileIdle(
                    AlarmManager.RTC_WAKEUP,
                    task.deadlineDateTime,
                    pendingDeadline
                )
            } catch (e: SecurityException) {
                e.printStackTrace()
            }
        }
    }
    
    fun cancelAlarmsForTask(context: Context, taskId: String) {
        val alarmManager = context.getSystemService(Context.ALARM_SERVICE) as AlarmManager
        
        val reachedIntent = Intent(context, TimerAlarmReceiver::class.java)
        val pendingReached = PendingIntent.getBroadcast(
            context, taskId.hashCode(), reachedIntent,
            PendingIntent.FLAG_NO_CREATE or PendingIntent.FLAG_IMMUTABLE
        )
        if (pendingReached != null) {
            alarmManager.cancel(pendingReached)
            pendingReached.cancel()
        }
        
        val approachingIntent = Intent(context, TimerAlarmReceiver::class.java)
        val approachingRequestCode = (taskId + "_approaching").hashCode()
        val pendingApproaching = PendingIntent.getBroadcast(
            context, approachingRequestCode, approachingIntent,
            PendingIntent.FLAG_NO_CREATE or PendingIntent.FLAG_IMMUTABLE
        )
        if (pendingApproaching != null) {
            alarmManager.cancel(pendingApproaching)
            pendingApproaching.cancel()
        }

        val deadlineIntent = Intent(context, TimerAlarmReceiver::class.java)
        val deadlineRequestCode = (taskId + "_deadline").hashCode()
        val pendingDeadline = PendingIntent.getBroadcast(
            context, deadlineRequestCode, deadlineIntent,
            PendingIntent.FLAG_NO_CREATE or PendingIntent.FLAG_IMMUTABLE
        )
        if (pendingDeadline != null) {
            alarmManager.cancel(pendingDeadline)
            pendingDeadline.cancel()
        }
    }
}
