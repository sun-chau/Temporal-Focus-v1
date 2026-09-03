with open("app/src/main/java/com/example/data/TrackerDao.kt", "r") as f:
    content = f.read()

if "getTrackerById" not in content:
    new_query = """    @Query("SELECT * FROM trackers WHERE id = :id")
    fun getTrackerById(id: String): Flow<TrackerEntity?>

    @Insert"""
    content = content.replace("    @Insert", new_query)
    with open("app/src/main/java/com/example/data/TrackerDao.kt", "w") as f:
        f.write(content)
