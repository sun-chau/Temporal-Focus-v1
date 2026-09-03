import re

with open("app/src/main/java/com/example/ui/screens/BurnRateTrackerUI.kt", "r") as f:
    content = f.read()

# Add import
if "import androidx.compose.foundation.BorderStroke" not in content:
    content = content.replace("import androidx.compose.foundation.border", "import androidx.compose.foundation.border\nimport androidx.compose.foundation.BorderStroke")

# Add state variable
content = content.replace("var showAddTagDialog by remember { mutableStateOf(false) }", "var showAddTagDialog by remember { mutableStateOf(false) }\n    var tagToDelete by remember { mutableStateOf<String?>(null) }")

# Replace Tags section
tags_old = """        // Tags
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .horizontalScroll(rememberScrollState()),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            tags.forEach { tag ->
                FilterChip(
                    selected = selectedTag == tag,
                    onClick = { selectedTag = tag },
                    label = { Text(tag) }
                )
            }
            FilterChip(
                selected = false,
                onClick = { showAddTagDialog = true },
                label = { Text("+ TAG") }
            )
        }"""

tags_new = """        // Tags
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .horizontalScroll(rememberScrollState()),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            val defaultTags = listOf("GENERAL", "FOOD", "TRANSPORT")
            defaultTags.forEach { tag ->
                FilterChip(
                    selected = selectedTag == tag,
                    onClick = { selectedTag = tag },
                    label = { Text(tag) }
                )
            }
            payload.customTags.forEach { tag ->
                Surface(
                    modifier = Modifier
                        .combinedClickable(
                            onClick = { selectedTag = tag },
                            onLongClick = { tagToDelete = tag }
                        ),
                    shape = MaterialTheme.shapes.small,
                    color = if (selectedTag == tag) MaterialTheme.colorScheme.secondaryContainer else MaterialTheme.colorScheme.surface,
                    border = BorderStroke(1.dp, if (selectedTag == tag) MaterialTheme.colorScheme.secondaryContainer else MaterialTheme.colorScheme.outline)
                ) {
                    Text(
                        text = tag,
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                        style = MaterialTheme.typography.labelLarge,
                        color = if (selectedTag == tag) MaterialTheme.colorScheme.onSecondaryContainer else MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
            FilterChip(
                selected = false,
                onClick = { showAddTagDialog = true },
                label = { Text("+ TAG") }
            )
        }"""
content = content.replace(tags_old, tags_new)

# Add Delete Modal
delete_modal = """
    if (tagToDelete != null) {
        val tag = tagToDelete!!
        AlertDialog(
            onDismissRequest = { tagToDelete = null },
            title = { Text("Delete Tag") },
            text = { Text("Are you sure you want to delete the tag '[ $tag ]'? This will not delete past transactions using this tag.") },
            confirmButton = {
                TextButton(
                    onClick = {
                        viewModel.deleteBurnRateTag(entity, tag)
                        if (selectedTag == tag) {
                            selectedTag = "GENERAL"
                        }
                        tagToDelete = null
                    }
                ) { Text("DELETE", color = MaterialTheme.colorScheme.error, fontWeight = FontWeight.Bold) }
            },
            dismissButton = {
                TextButton(onClick = { tagToDelete = null }) { Text("CANCEL") }
            }
        )
    }
}"""
content = re.sub(r'}\s*$', delete_modal, content)

with open("app/src/main/java/com/example/ui/screens/BurnRateTrackerUI.kt", "w") as f:
    f.write(content)

