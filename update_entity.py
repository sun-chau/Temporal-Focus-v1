with open("app/src/main/java/com/example/data/TrackerEntity.kt", "r") as f:
    content = f.read()

content = content.replace(
    "data class BurnRatePayload(val monthlyLimit: Int = 0, val transactions: List<Transaction> = emptyList())",
    "data class BurnRatePayload(val monthlyLimit: Double = 0.0, val customTags: Set<String> = emptySet(), val transactions: List<Transaction> = emptyList())"
)

content = content.replace(
    "data class Transaction(val id: String, val amountInr: Int, val timestampEpoch: Long, val tag: String)",
    "data class Transaction(val id: String, val amount: Double, val timestampEpoch: Long, val tag: String)"
)

with open("app/src/main/java/com/example/data/TrackerEntity.kt", "w") as f:
    f.write(content)
