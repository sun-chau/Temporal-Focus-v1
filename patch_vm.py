import re

with open("app/src/main/java/com/example/viewmodel/TrackerViewModel.kt", "r") as f:
    content = f.read()

# 1. Update getParsedPayload
parsing_old = """                TrackerType.ASSIGNMENT -> {
                    val p = json?.let { gson.fromJson(it, AssignmentPayload::class.java) } ?: AssignmentPayload()
                    p.copy(tasks = p.tasks ?: emptyList())
                }
            }"""

parsing_new = """                TrackerType.ASSIGNMENT -> {
                    val p = json?.let { gson.fromJson(it, AssignmentPayload::class.java) } ?: AssignmentPayload()
                    p.copy(tasks = p.tasks ?: emptyList())
                }
                TrackerType.BINARY -> {
                    val p = json?.let { gson.fromJson(it, BinaryPayload::class.java) } ?: BinaryPayload()
                    p.copy(disciplines = p.disciplines ?: emptyList())
                }
                TrackerType.VOLUME -> {
                    val p = json?.let { gson.fromJson(it, VolumePayload::class.java) } ?: VolumePayload()
                    p.copy(resources = p.resources ?: emptyList())
                }
                TrackerType.BURN_RATE -> {
                    val p = json?.let { gson.fromJson(it, BurnRatePayload::class.java) } ?: BurnRatePayload()
                    p.copy(transactions = p.transactions ?: emptyList())
                }
            }"""
content = content.replace(parsing_old, parsing_new)

# 2. Update getTelemetryString
telemetry_old = """                TrackerType.CUSTOM -> {
                    "[ CUSTOM TRACKER ]"
                }
            }"""

telemetry_new = """                TrackerType.CUSTOM -> {
                    "[ CUSTOM TRACKER ]"
                }
                TrackerType.BINARY -> {
                    val p = payload as? BinaryPayload ?: BinaryPayload()
                    "[ ${p.disciplines.size} DISCIPLINES ]"
                }
                TrackerType.VOLUME -> {
                    val p = payload as? VolumePayload ?: VolumePayload()
                    val activeCount = p.resources.count { it.currentProgress < it.totalProgress }
                    "[ $activeCount ACTIVE RESOURCES ]"
                }
                TrackerType.BURN_RATE -> {
                    val p = payload as? BurnRatePayload ?: BurnRatePayload()
                    val currentMonth = java.time.YearMonth.now()
                    val monthlySum = p.transactions.filter { 
                        val dateTime = java.time.Instant.ofEpochMilli(it.timestampEpoch).atZone(java.time.ZoneId.systemDefault()).toLocalDate()
                        java.time.YearMonth.from(dateTime) == currentMonth
                    }.sumOf { it.amountInr }
                    "[ ₹$monthlySum / ₹${p.monthlyLimit} BURNED ]"
                }
            }"""
content = content.replace(telemetry_old, telemetry_new)

# 3. Add updatePayload functions for the 3 new types
updates_new = """
    fun updateBinaryPayload(entity: TrackerEntity, payload: BinaryPayload) {
        val newData = gson.toJson(payload)
        updateTracker(entity.copy(payloadData = newData, lastModified = System.currentTimeMillis()))
    }
    fun updateVolumePayload(entity: TrackerEntity, payload: VolumePayload) {
        val newData = gson.toJson(payload)
        updateTracker(entity.copy(payloadData = newData, lastModified = System.currentTimeMillis()))
    }
    fun updateBurnRatePayload(entity: TrackerEntity, payload: BurnRatePayload) {
        val newData = gson.toJson(payload)
        updateTracker(entity.copy(payloadData = newData, lastModified = System.currentTimeMillis()))
    }
"""

if "updateBinaryPayload" not in content:
    content = content.replace("    fun getTrackerById(id: String) = trackerDao.getTrackerById(id)", updates_new + "    fun getTrackerById(id: String) = trackerDao.getTrackerById(id)")

with open("app/src/main/java/com/example/viewmodel/TrackerViewModel.kt", "w") as f:
    f.write(content)

