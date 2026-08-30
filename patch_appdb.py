import re

with open("app/src/main/java/com/example/data/AppDatabase.kt", "r") as f:
    content = f.read()

target = """                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "temporal_focus_db"
                )
                .fallbackToDestructiveMigration()
                .build()"""

replacement = """                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "temporal_focus_db"
                )
                .fallbackToDestructiveMigration()
                .addCallback(object : RoomDatabase.Callback() {
                    override fun onCreate(db: androidx.sqlite.db.SupportSQLiteDatabase) {
                        super.onCreate(db)
                        kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch {
                            val dao = INSTANCE?.dailyScheduleDao()
                            dao?.let {
                                MockDataGenerator.getMockTasks().forEach { task ->
                                    it.insertSchedule(task)
                                }
                            }
                        }
                    }
                })
                .build()"""

content = content.replace(target, replacement)

# Add imports for coroutines if not exists
if "import kotlinx.coroutines.launch" not in content:
    content = content.replace("import androidx.room.RoomDatabase", "import androidx.room.RoomDatabase\nimport kotlinx.coroutines.launch")

with open("app/src/main/java/com/example/data/AppDatabase.kt", "w") as f:
    f.write(content)
