import re

with open("app/src/main/java/com/example/ui/screens/UserAccountScreen.kt", "r") as f:
    content = f.read()

# Add imports
content = content.replace("import androidx.compose.material.icons.filled.ArrowBack", "import androidx.compose.material.icons.filled.*")
content = content.replace("import androidx.compose.foundation.lazy.LazyColumn", "import androidx.compose.foundation.lazy.LazyColumn\nimport androidx.compose.foundation.rememberScrollState\nimport androidx.compose.foundation.verticalScroll")
content = content.replace("import androidx.compose.ui.unit.dp", "import androidx.compose.ui.unit.dp\nimport androidx.compose.ui.unit.sp\nimport androidx.compose.foundation.BorderStroke")

# Add state variables
state_vars = """    var name by remember { mutableStateOf(uiState.profileName) }
    var bio by remember { mutableStateOf(uiState.profileBio) }
    var imageUri by remember { mutableStateOf(uiState.profileImageUri) }
    var newTag by remember { mutableStateOf("") }
    var tagColor by remember { mutableStateOf(String.format("#%02X%02X%02X", (0..255).random(), (0..255).random(), (0..255).random())) }
    var showAddFieldDialog by remember { mutableStateOf(false) }
    var showManageFieldsDialog by remember { mutableStateOf(false) }"""
content = re.sub(r'    var name by remember \{ mutableStateOf\(uiState.profileName\) \}\n    var bio by remember \{ mutableStateOf\(uiState.profileBio\) \}\n    var imageUri by remember \{ mutableStateOf\(uiState.profileImageUri\) \}\n    var newTag by remember \{ mutableStateOf\(""\) \}', state_vars, content)

# Update Profile Details to include Custom Fields buttons
profile_details = """            item {
                // Profile Details
                OutlinedTextField(
                    value = name,
                    onValueChange = { name = it },
                    label = { Text("Name") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true
                )
                Spacer(modifier = Modifier.height(16.dp))
                OutlinedTextField(
                    value = bio,
                    onValueChange = { bio = it },
                    label = { Text("Bio / Additional Info") },
                    modifier = Modifier.fillMaxWidth(),
                    minLines = 3,
                    maxLines = 5
                )
                Spacer(modifier = Modifier.height(16.dp))
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = { showAddFieldDialog = true }, modifier = Modifier.weight(1f)) {
                        Icon(Icons.Default.Input, contentDescription = "Custom Fields")
                        Spacer(Modifier.width(8.dp))
                        Text("Custom Field")
                    }
                    Button(onClick = { showManageFieldsDialog = true }, modifier = Modifier.weight(1f)) {
                        Icon(Icons.Default.Badge, contentDescription = "Manage Fields")
                        Spacer(Modifier.width(8.dp))
                        Text("Manage Fields")
                    }
                }
            }"""
content = re.sub(r'            item \{\s*// Profile Details\s*OutlinedTextField\([^)]+\)\s*Spacer\(modifier = Modifier\.height\(16\.dp\)\)\s*OutlinedTextField\([^)]+\)\s*\}', profile_details, content)

# Update Tag Manager
tag_manager = """                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    OutlinedTextField(
                        value = newTag,
                        onValueChange = { newTag = it },
                        label = { Text("New Tag") },
                        modifier = Modifier.weight(1f),
                        singleLine = true,
                        trailingIcon = {
                            Box(
                                modifier = Modifier
                                    .size(24.dp)
                                    .clip(CircleShape)
                                    .background(try { Color(android.graphics.Color.parseColor(tagColor)) } catch(e:Exception){Color.Gray})
                                    .clickable { tagColor = String.format("#%02X%02X%02X", (0..255).random(), (0..255).random(), (0..255).random()) }
                            )
                        }
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Button(onClick = {
                        if (newTag.isNotBlank()) {
                            viewModel.addCustomTag("${newTag.trim()}|$tagColor")
                            newTag = ""
                            tagColor = String.format("#%02X%02X%02X", (0..255).random(), (0..255).random(), (0..255).random())
                        }
                    }, contentPadding = PaddingValues(0.dp), modifier = Modifier.size(48.dp).padding(4.dp)) {
                        Icon(Icons.Default.Add, contentDescription = "Add")
                    }
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                
                // Display Tags
                @OptIn(ExperimentalLayoutApi::class)
                FlowRow(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    uiState.customTags.forEach { tag ->
                        val parts = tag.split("|", limit = 2)
                        val tagName = parts[0]
                        val colorStr = parts.getOrNull(1) ?: "#00000000"
                        val tagColorValue = try { Color(android.graphics.Color.parseColor(colorStr)) } catch (e: Exception) { Color.Transparent }
                        
                        AssistChip(
                            onClick = { },
                            label = { Text(tagName) },
                            border = BorderStroke(2.dp, if (tagColorValue != Color.Transparent) tagColorValue else MaterialTheme.colorScheme.outline),
                            trailingIcon = {
                                IconButton(
                                    onClick = { viewModel.removeCustomTag(tag) },
                                    modifier = Modifier.size(16.dp)
                                ) {
                                    Icon(
                                        Icons.Default.Close,
                                        contentDescription = "Remove Tag",
                                        modifier = Modifier.size(12.dp),
                                        tint = if (tagColorValue != Color.Transparent) tagColorValue else LocalContentColor.current
                                    )
                                }
                            }
                        )
                    }
                }"""
content = re.sub(r'                Row\([^)]+\) \{\s*OutlinedTextField\([^)]+\)\s*Spacer\(modifier = Modifier\.width\(8\.dp\)\)\s*Button\(onClick = \{[^}]+\}\) \{\s*Text\("Add"\)\s*\}\s*\}\s*Spacer\(modifier = Modifier\.height\(16\.dp\)\)\s*// Display Tags\s*@OptIn\(ExperimentalLayoutApi::class\)\s*FlowRow\([^)]+\) \{\s*uiState\.customTags\.forEach \{ tag ->\s*AssistChip\([^)]+\)\s*\}\s*\}', tag_manager, content)

# Add Dialogs at the end
dialogs = """
    if (showAddFieldDialog) {
        var fieldName by remember { mutableStateOf("") }
        var fieldValue by remember { mutableStateOf("") }
        AlertDialog(
            onDismissRequest = { showAddFieldDialog = false },
            title = { Text("Add Custom Field") },
            text = {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedTextField(value = fieldName, onValueChange = { fieldName = it }, label = { Text("Field Name") })
                    OutlinedTextField(value = fieldValue, onValueChange = { fieldValue = it }, label = { Text("Field Value") })
                }
            },
            confirmButton = {
                Button(onClick = { 
                    if (fieldName.isNotBlank() && fieldValue.isNotBlank()) {
                        viewModel.addProfileCustomField(fieldName.trim(), fieldValue.trim())
                        showAddFieldDialog = false
                    }
                }) { Text("Add") }
            },
            dismissButton = {
                TextButton(onClick = { showAddFieldDialog = false }) { Text("Cancel") }
            }
        )
    }

    if (showManageFieldsDialog) {
        AlertDialog(
            onDismissRequest = { showManageFieldsDialog = false },
            title = { Text("Manage Custom Fields") },
            text = {
                Column(modifier = Modifier.fillMaxWidth().heightIn(max = 300.dp).verticalScroll(rememberScrollState())) {
                    uiState.profileCustomFields.forEach { (key, value) ->
                        var isEditing by remember { mutableStateOf(false) }
                        if (isEditing) {
                            var editKey by remember { mutableStateOf(key) }
                            var editValue by remember { mutableStateOf(value) }
                            Column(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                                OutlinedTextField(value = editKey, onValueChange = { editKey = it }, label = { Text("Field") })
                                OutlinedTextField(value = editValue, onValueChange = { editValue = it }, label = { Text("Value") })
                                Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.align(Alignment.End)) {
                                    TextButton(onClick = { isEditing = false }) { Text("Cancel") }
                                    Button(onClick = { 
                                        if (editKey.isNotBlank() && editValue.isNotBlank()) {
                                            viewModel.updateProfileCustomField(key, editKey.trim(), editValue.trim())
                                            isEditing = false
                                        }
                                    }) { Text("Save") }
                                }
                            }
                        } else {
                            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                Column(modifier = Modifier.weight(1f)) {
                                    Text(key, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                                    Text(value, fontSize = 14.sp)
                                }
                                Row {
                                    IconButton(onClick = { isEditing = true }) { Icon(Icons.Default.Edit, contentDescription = "Edit") }
                                    IconButton(onClick = { viewModel.removeProfileCustomField(key) }) { Icon(Icons.Default.Delete, contentDescription = "Delete") }
                                }
                            }
                        }
                        HorizontalDivider()
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = { showManageFieldsDialog = false }) { Text("Close") }
            }
        )
    }
}"""
content = content.replace("    }\n}\n", "    }\n" + dialogs + "\n")

with open("app/src/main/java/com/example/ui/screens/UserAccountScreen.kt", "w") as f:
    f.write(content)
