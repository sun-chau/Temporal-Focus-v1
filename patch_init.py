import re

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()

target1 = """    init {
        performRollingRefill()
        val database = AppDatabase.getDatabase(application)"""
replacement1 = """    init {
        val database = AppDatabase.getDatabase(application)"""

target2 = """        repository = TimerTaskRepository(database.timerTaskDao())
        appSettings = AppSettings(application)
        
        activeTasks = repository.activeTasks.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())"""
replacement2 = """        repository = TimerTaskRepository(database.timerTaskDao())
        appSettings = AppSettings(application)
        performRollingRefill()
        
        activeTasks = repository.activeTasks.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())"""

content = content.replace(target1, replacement1).replace(target2, replacement2)

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
    f.write(content)
