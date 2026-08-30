package com.example.receiver

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.media.RingtoneManager
import android.os.Build
import android.os.VibrationEffect
import android.os.Vibrator
import android.os.VibratorManager
import android.util.Log
import androidx.core.app.NotificationCompat
import androidx.core.content.ContextCompat
import com.example.MainActivity
import com.example.R
import com.example.data.AppDatabase
import com.example.data.TimerTask
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

class TimerAlarmReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        val taskId = intent.getStringExtra("TASK_ID") ?: return
        val isApproaching = intent.getBooleanExtra("IS_APPROACHING", false)
        val isDeadline = intent.getBooleanExtra("IS_DEADLINE", false)
        val offsetMinutes = intent.getIntExtra("OFFSET_MINUTES", 0)
        
        Log.d("TimerAlarmReceiver", "Received alarm for task: $taskId, approaching: $isApproaching, deadline: $isDeadline")
        
        val db = AppDatabase.getDatabase(context)
        val repo = com.example.data.TimerTaskRepository(db.timerTaskDao())
        
        CoroutineScope(Dispatchers.IO).launch {
            val task = repo.getTaskByIdSync(taskId)
            if (task != null && !task.isCompleted) {
                if (isDeadline) {
                    playChronometerAlert(context, task, false, 0, isDeadline = true)
                } else {
                    if (!isApproaching && System.currentTimeMillis() < task.targetDateTime - 60000) {
                        // ignore drift
                    }
                    playChronometerAlert(context, task, isApproaching, offsetMinutes, isDeadline = false)
                }
            }
        }
    }

    private fun playChronometerAlert(context: Context, task: TimerTask, isApproaching: Boolean, offsetMinutes: Int = 0, isDeadline: Boolean = false) {
        val taskName = task.name
        
        val notificationManager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel("chronometer", "Chronometer Alerts", NotificationManager.IMPORTANCE_HIGH)
            notificationManager.createNotificationChannel(channel)
        }
        
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.TIRAMISU || 
            ContextCompat.checkSelfPermission(context, android.Manifest.permission.POST_NOTIFICATIONS) == android.content.pm.PackageManager.PERMISSION_GRANTED) {
            
            val notificationId = task.id.hashCode()
            
            val openIntent = Intent(context, MainActivity::class.java).apply {
                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
            }
            val pendingOpenIntent = PendingIntent.getActivity(
                context, notificationId, openIntent, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )

            val completeIntent = Intent(context, NotificationActionReceiver::class.java).apply {
                action = "MARK_COMPLETE"
                putExtra("TASK_ID", task.id)
                putExtra("NOTIFICATION_ID", notificationId)
            }
            val pendingCompleteIntent = PendingIntent.getBroadcast(
                context, notificationId + 1, completeIntent, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )

            val snoozeIntent = Intent(context, NotificationActionReceiver::class.java).apply {
                action = "SNOOZE"
                putExtra("TASK_ID", task.id)
                putExtra("NOTIFICATION_ID", notificationId)
            }
            val pendingSnoozeIntent = PendingIntent.getBroadcast(
                context, notificationId + 2, snoozeIntent, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
            
            val themeColor = Color.parseColor("#90CAF9") // Default Midnight Minimalist, could read from prefs if we had SharedPreferences
            
            val tagsLower = task.labels.lowercase()
            val largeIconId = when {
                "work" in tagsLower -> android.R.drawable.ic_menu_manage
                "fitness" in tagsLower || "health" in tagsLower -> android.R.drawable.ic_menu_myplaces
                "study" in tagsLower -> android.R.drawable.ic_menu_sort_by_size
                "personal" in tagsLower -> android.R.drawable.ic_menu_my_calendar
                else -> null
            }
            
            val builder = NotificationCompat.Builder(context, "chronometer")
                .setSmallIcon(R.drawable.ic_launcher_foreground)
                .setAutoCancel(true)
                .setContentIntent(pendingOpenIntent)
                .setUsesChronometer(true)
                .setWhen(task.targetDateTime)
                .setColor(themeColor)
                
            if (largeIconId != null) {
                builder.setLargeIcon(getBitmapFromVectorDrawable(context, largeIconId))
            }
                
            if (isDeadline) {
                builder.setContentTitle("Reminder: $taskName")
                builder.setContentText("Due now!")
                builder.setPriority(NotificationCompat.PRIORITY_HIGH)
                builder.addAction(R.drawable.ic_launcher_foreground, "View Details", pendingOpenIntent)
                builder.addAction(R.drawable.ic_launcher_foreground, "Mark Complete", pendingCompleteIntent)
            } else if (isApproaching) {
                builder.setContentTitle("Upcoming: $taskName")
                builder.setContentText("Ends in $offsetMinutes minutes.")
                builder.setPriority(NotificationCompat.PRIORITY_DEFAULT)
                
                val bigTextStyle = NotificationCompat.BigTextStyle()
                if (task.description.isNullOrEmpty()) {
                    bigTextStyle.bigText("Ends in $offsetMinutes minutes.")
                } else {
                    bigTextStyle.bigText("${task.name}\n${task.description}")
                }
                builder.setStyle(bigTextStyle)
                builder.addAction(R.drawable.ic_launcher_foreground, "Mark Complete", pendingCompleteIntent)
                builder.addAction(R.drawable.ic_launcher_foreground, "Snooze", pendingSnoozeIntent)
            } else {
                builder.setContentTitle("Time's Up!")
                builder.setContentText("\"$taskName\" has reached its target time.")
                builder.setPriority(NotificationCompat.PRIORITY_HIGH)
                
                builder.addAction(R.drawable.ic_launcher_foreground, "View Details", pendingOpenIntent)
                builder.addAction(R.drawable.ic_launcher_foreground, "Mark Complete", pendingCompleteIntent)
            }

            notificationManager.notify(notificationId, builder.build())
        }

        try {
            val uri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION)
            val ringtone = RingtoneManager.getRingtone(context, uri)
            ringtone.play()
        } catch (e: Exception) {
            e.printStackTrace()
        }
        
        vibrate(context)
    }

    private fun getBitmapFromVectorDrawable(context: Context, drawableId: Int): Bitmap {
        val drawable = ContextCompat.getDrawable(context, drawableId) ?: return Bitmap.createBitmap(1, 1, Bitmap.Config.ARGB_8888)
        val bitmap = Bitmap.createBitmap(
            drawable.intrinsicWidth,
            drawable.intrinsicHeight,
            Bitmap.Config.ARGB_8888
        )
        val canvas = Canvas(bitmap)
        drawable.setBounds(0, 0, canvas.width, canvas.height)
        drawable.draw(canvas)
        return bitmap
    }
    
    private fun vibrate(context: Context) {
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                val vibratorManager = context.getSystemService(Context.VIBRATOR_MANAGER_SERVICE) as VibratorManager
                val vibrator = vibratorManager.defaultVibrator
                vibrator.vibrate(VibrationEffect.createOneShot(500, VibrationEffect.DEFAULT_AMPLITUDE))
            } else {
                @Suppress("DEPRECATION")
                val vibrator = context.getSystemService(Context.VIBRATOR_SERVICE) as Vibrator
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    vibrator.vibrate(VibrationEffect.createOneShot(500, VibrationEffect.DEFAULT_AMPLITUDE))
                } else {
                    @Suppress("DEPRECATION")
                    vibrator.vibrate(500)
                }
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
}
