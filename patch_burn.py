import re

with open("app/src/main/java/com/example/ui/screens/BurnRateTrackerUI.kt", "r") as f:
    content = f.read()

limit_btn_old = """            confirmButton = {
                TextButton(
                    onClick = {
                        val limit = limitInput.toDoubleOrNull() ?: 0.0
                        viewModel.updateBurnRatePayload(entity, payload.copy(monthlyLimit = limit))
                        showLimitDialog = false
                    }
                ) { Text("SAVE") }
            },"""
limit_btn_new = """            confirmButton = {
                val hasChanges = (limitInput.toDoubleOrNull() ?: 0.0) != payload.monthlyLimit
                TextButton(
                    onClick = {
                        val limit = limitInput.toDoubleOrNull() ?: 0.0
                        viewModel.updateBurnRatePayload(entity, payload.copy(monthlyLimit = limit))
                        showLimitDialog = false
                    },
                    enabled = hasChanges
                ) { Text(if (hasChanges) "SAVE CHANGES" else "NO CHANGES", fontWeight = FontWeight.Bold) }
            },"""
content = content.replace(limit_btn_old, limit_btn_new)

tag_btn_old = """            confirmButton = {
                TextButton(
                    onClick = {
                        if (newTagInput.isNotBlank()) {
                            viewModel.addBurnRateTag(entity, newTagInput)
                        }
                        showAddTagDialog = false
                    }
                ) { Text("SAVE") }
            },"""
tag_btn_new = """            confirmButton = {
                val hasChanges = newTagInput.isNotBlank()
                TextButton(
                    onClick = {
                        if (newTagInput.isNotBlank()) {
                            viewModel.addBurnRateTag(entity, newTagInput)
                        }
                        showAddTagDialog = false
                    },
                    enabled = hasChanges
                ) { Text(if (hasChanges) "SAVE CHANGES" else "NO CHANGES", fontWeight = FontWeight.Bold) }
            },"""
content = content.replace(tag_btn_old, tag_btn_new)

with open("app/src/main/java/com/example/ui/screens/BurnRateTrackerUI.kt", "w") as f:
    f.write(content)

