import re

with open("app/src/main/java/com/example/viewmodel/TrackerViewModel.kt", "r") as f:
    content = f.read()

# Update getParsedPayload
parse_old = """                TrackerType.BURN_RATE -> {
                    val p = json?.let { gson.fromJson(it, BurnRatePayload::class.java) } ?: BurnRatePayload()
                    p.copy(transactions = p.transactions ?: emptyList())
                }"""
parse_new = """                TrackerType.BURN_RATE -> {
                    val p = json?.let { gson.fromJson(it, BurnRatePayload::class.java) } ?: BurnRatePayload()
                    p.copy(transactions = p.transactions ?: emptyList(), customTags = p.customTags ?: emptySet())
                }"""
content = content.replace(parse_old, parse_new)

# Update getTelemetryString
telemetry_old = """                TrackerType.BURN_RATE -> {
                    val p = payload as? BurnRatePayload ?: BurnRatePayload()
                    val currentMonth = java.time.YearMonth.now()
                    val monthlySum = p.transactions.filter { 
                        val dateTime = java.time.Instant.ofEpochMilli(it.timestampEpoch).atZone(java.time.ZoneId.systemDefault()).toLocalDate()
                        java.time.YearMonth.from(dateTime) == currentMonth
                    }.sumOf { it.amountInr }
                    "[ ₹$monthlySum / ₹${p.monthlyLimit} BURNED ]"
                }"""
telemetry_new = """                TrackerType.BURN_RATE -> {
                    val p = payload as? BurnRatePayload ?: BurnRatePayload()
                    val currentMonth = java.time.YearMonth.now()
                    val monthlySum = p.transactions.filter { 
                        val dateTime = java.time.Instant.ofEpochMilli(it.timestampEpoch).atZone(java.time.ZoneId.systemDefault()).toLocalDate()
                        java.time.YearMonth.from(dateTime) == currentMonth
                    }.sumOf { it.amount }
                    "[ ₹%.2f / ₹%.2f BURNED ]".format(monthlySum, p.monthlyLimit)
                }"""
content = content.replace(telemetry_old, telemetry_new)

# Add addBurnRateTag
tag_func = """
    fun addBurnRateTag(tracker: TrackerEntity, newTag: String) {
        val payload = getParsedPayload(tracker) as? BurnRatePayload ?: return
        val updatedTags = payload.customTags + newTag.uppercase()
        updateBurnRatePayload(tracker, payload.copy(customTags = updatedTags))
    }
"""
if "fun addBurnRateTag" not in content:
    content = content.replace("    fun updateBurnRatePayload", tag_func + "    fun updateBurnRatePayload")

with open("app/src/main/java/com/example/viewmodel/TrackerViewModel.kt", "w") as f:
    f.write(content)

