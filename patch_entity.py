import re

with open("app/src/main/java/com/example/data/TrackerEntity.kt", "r") as f:
    content = f.read()

old_schema = "data class BurnRatePayload(val monthlyLimit: Double = 0.0, val customTags: Set<String> = emptySet(), val transactions: List<Transaction> = emptyList())"
new_schema = "data class BurnRatePayload(val monthlyLimit: Double = 0.0, val cycleStartDay: Int = 1, val customTags: Set<String> = emptySet(), val transactions: List<Transaction> = emptyList())"

content = content.replace(old_schema, new_schema)

with open("app/src/main/java/com/example/data/TrackerEntity.kt", "w") as f:
    f.write(content)
