with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

content = content.replace("private fun recalculateAllLanes(db: com.example.data.AppDatabase)", "private suspend fun recalculateAllLanes(db: com.example.data.AppDatabase)")

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
