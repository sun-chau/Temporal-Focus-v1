import re

# AppDatabase.kt
with open('app/src/main/java/com/example/data/AppDatabase.kt', 'r') as f:
    content = f.read()

target_db = """                            val dao = INSTANCE?.dailyScheduleDao()
                            dao?.let {
                                MockDataGenerator.getMockTasks().forEach { task ->
                                    it.insertSchedule(task)
                                }
                            }"""

replacement_db = """                            // Mock data generation removed"""
content = content.replace(target_db, replacement_db)

with open('app/src/main/java/com/example/data/AppDatabase.kt', 'w') as f:
    f.write(content)

# MainViewModel.kt
with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()

target_vm = """            val schedules = database.dailyScheduleDao().getAllSchedulesSync()
            if (schedules.isEmpty()) {
                com.example.data.MockDataGenerator.getMockTasks().forEach {
                    database.dailyScheduleDao().insertSchedule(it)
                }
            }"""

replacement_vm = """            // Mock schedules removed"""
content = content.replace(target_vm, replacement_vm)

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
    f.write(content)
