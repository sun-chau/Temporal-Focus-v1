package com.example.data

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import kotlinx.coroutines.launch

@Database(entities = [TimerTask::class, FocusSessionStats::class, DailyScheduleTask::class, JournalEntry::class, JournalTemplate::class, TrackerEntity::class, TrackerLogEntity::class], version = 15, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    abstract fun timerTaskDao(): TimerTaskDao
    abstract fun focusSessionStatsDao(): FocusSessionStatsDao
    abstract fun dailyScheduleDao(): DailyScheduleDao
    
    abstract fun journalDao(): JournalDao
    abstract fun trackerDao(): TrackerDao

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun getDatabase(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "temporal_focus_db"
                )
                .fallbackToDestructiveMigration(true)
                .addCallback(object : RoomDatabase.Callback() {
                    override fun onCreate(db: androidx.sqlite.db.SupportSQLiteDatabase) {
                        super.onCreate(db)
                        kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch {
                            // Mock data generation removed
                        }
                    }
                })
                .build()
                INSTANCE = instance
                instance
            }
        }
    }
}
