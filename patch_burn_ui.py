import re

with open("app/src/main/java/com/example/ui/screens/BurnRateTrackerUI.kt", "r") as f:
    content = f.read()

# 1. State variable
state_old = """    var tagToDelete by remember { mutableStateOf<String?>(null) }"""
state_new = """    var tagToDelete by remember { mutableStateOf<String?>(null) }
    var transactionToDelete by remember { mutableStateOf<Transaction?>(null) }"""
content = content.replace(state_old, state_new)

# 2. monthlySum -> activeMonthTx & monthlySum
sum_old = """    val monthlySum = payload.transactions.filter {
        val dateTime = java.time.Instant.ofEpochMilli(it.timestampEpoch).atZone(java.time.ZoneId.systemDefault()).toLocalDate()
        java.time.YearMonth.from(dateTime) == currentMonth
    }.sumOf { it.amount }"""

sum_new = """    val activeMonthTx = payload.transactions.filter {
        val dateTime = java.time.Instant.ofEpochMilli(it.timestampEpoch).atZone(java.time.ZoneId.systemDefault()).toLocalDate()
        java.time.YearMonth.from(dateTime) == currentMonth
    }.sortedByDescending { it.timestampEpoch }
    val monthlySum = activeMonthTx.sumOf { it.amount }"""
content = content.replace(sum_old, sum_new)

# 3. items(payload.transactions -> items(activeMonthTx
items_old = """            items(payload.transactions, key = { it.id }) { tx ->"""
items_new = """            items(activeMonthTx, key = { it.id }) { tx ->"""
content = content.replace(items_old, items_new)

# 4. Long click
long_click_old = """                            onLongClick = {
                                val updated = payload.transactions.filter { it.id != tx.id }
                                viewModel.updateBurnRatePayload(entity, payload.copy(transactions = updated))
                            }"""
long_click_new = """                            onLongClick = {
                                transactionToDelete = tx
                            }"""
content = content.replace(long_click_old, long_click_new)

# 5. Numpad logic
numpad_old = """                            if (key == "DEDUCT") {
                                val amt = inputStr.toDoubleOrNull() ?: 0.0
                                if (amt > 0.0) {
                                    val newTx = Transaction(
                                        id = UUID.randomUUID().toString(),
                                        amount = amt,
                                        timestampEpoch = System.currentTimeMillis(),
                                        tag = selectedTag
                                    )
                                    viewModel.updateBurnRatePayload(
                                        entity,
                                        payload.copy(transactions = listOf(newTx) + payload.transactions)
                                    )
                                    inputStr = ""
                                }
                            } else if (key == "DEL") {
                                if (inputStr.isNotEmpty()) inputStr = inputStr.dropLast(1)
                            } else if (key == ".") {
                                if (!inputStr.contains(".")) inputStr += "."
                            } else {
                                inputStr += key
                            }"""

numpad_new = """                            if (key == "DEDUCT") {
                                val amt = inputStr.toDoubleOrNull() ?: 0.0
                                if (amt > 0.0) {
                                    val newTx = Transaction(
                                        id = UUID.randomUUID().toString(),
                                        amount = amt,
                                        timestampEpoch = System.currentTimeMillis(),
                                        tag = selectedTag
                                    )
                                    viewModel.updateBurnRatePayload(
                                        entity,
                                        payload.copy(transactions = listOf(newTx) + payload.transactions)
                                    )
                                    inputStr = ""
                                } else {
                                    inputStr = ""
                                }
                            } else if (key == "DEL") {
                                if (inputStr.isNotEmpty()) inputStr = inputStr.dropLast(1)
                            } else if (key == ".") {
                                if (!inputStr.contains(".")) inputStr += "."
                            } else {
                                if (inputStr.contains(".") && inputStr.substringAfter(".", "").length >= 2) {
                                    // limit decimals
                                } else {
                                    inputStr += key
                                }
                            }"""
content = content.replace(numpad_old, numpad_new)

# 6. Delete dialog at the end
dialogs_old = """        )
    }
}"""
dialogs_new = """        )
    }

    if (transactionToDelete != null) {
        val tx = transactionToDelete!!
        AlertDialog(
            onDismissRequest = { transactionToDelete = null },
            title = { Text("Delete Transaction") },
            text = { Text("Are you sure you want to delete this transaction of ₹%.2f?".format(tx.amount)) },
            confirmButton = {
                TextButton(
                    onClick = {
                        val updated = payload.transactions.filter { it.id != tx.id }
                        viewModel.updateBurnRatePayload(entity, payload.copy(transactions = updated))
                        transactionToDelete = null
                    }
                ) { Text("DELETE", color = MaterialTheme.colorScheme.error, fontWeight = FontWeight.Bold) }
            },
            dismissButton = {
                TextButton(onClick = { transactionToDelete = null }) { Text("CANCEL") }
            }
        )
    }
}"""
content = content.replace(dialogs_old, dialogs_new)

with open("app/src/main/java/com/example/ui/screens/BurnRateTrackerUI.kt", "w") as f:
    f.write(content)

