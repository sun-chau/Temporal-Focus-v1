import re

with open("app/src/main/java/com/example/viewmodel/TrackerViewModel.kt", "r") as f:
    content = f.read()

new_funcs = """
    fun getActiveCycleTransactions(payload: BurnRatePayload): List<Transaction> {
        val now = java.time.ZonedDateTime.now()
        val currentDay = now.dayOfMonth
        val startDay = payload.cycleStartDay.coerceIn(1, 28)
        
        val cycleStart = if (currentDay >= startDay) {
            now.withDayOfMonth(startDay).withHour(0).withMinute(0).withSecond(0).withNano(0)
        } else {
            now.minusMonths(1).withDayOfMonth(startDay).withHour(0).withMinute(0).withSecond(0).withNano(0)
        }
        val cycleEnd = cycleStart.plusMonths(1)
        
        val startEpoch = cycleStart.toInstant().toEpochMilli()
        val endEpoch = cycleEnd.toInstant().toEpochMilli()
        
        return payload.transactions.filter { it.timestampEpoch in startEpoch until endEpoch }
    }

    fun updateTransaction(tracker: TrackerEntity, updatedTx: Transaction) {
        val payload = getParsedPayload(tracker) as? BurnRatePayload ?: return
        val newTxs = payload.transactions.map { if (it.id == updatedTx.id) updatedTx else it }
        updateBurnRatePayload(tracker, payload.copy(transactions = newTxs))
    }

    fun deleteTracker(tracker: TrackerEntity) {"""

content = content.replace("    fun deleteTracker(tracker: TrackerEntity) {", new_funcs)

with open("app/src/main/java/com/example/viewmodel/TrackerViewModel.kt", "w") as f:
    f.write(content)
