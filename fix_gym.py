import re
with open("app/src/main/java/com/example/ui/screens/GymTrackerUI.kt", "r") as f:
    content = f.read()

if "import androidx.compose.foundation.ExperimentalFoundationApi" not in content:
    content = content.replace("import androidx.compose.foundation.border", "import androidx.compose.foundation.ExperimentalFoundationApi\nimport androidx.compose.foundation.combinedClickable\nimport androidx.compose.foundation.border")

if "@OptIn(ExperimentalFoundationApi::class, ExperimentalMaterial3Api::class)" not in content:
    content = content.replace("@OptIn(ExperimentalMaterial3Api::class)", "@OptIn(ExperimentalFoundationApi::class, ExperimentalMaterial3Api::class)")

# 1. Update the row with combinedClickable
row_old = """                                    Row(
                                        modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Column(modifier = Modifier.weight(1f)) {
                                            Text("> ${ex.name.uppercase(Locale.getDefault())}", fontFamily = FontFamily.Monospace, fontWeight = FontWeight.Bold)
                                            val details = when (ex.type) {
                                                ExerciseType.REPS_ONLY -> "${ex.sets.size} SETS"
                                                ExerciseType.TIMED_DISTANCE -> "${ex.distanceMeters ?: 0}M IN ${ex.durationSeconds ?: 0}S"
                                                ExerciseType.STATIC_HOLD -> "${ex.durationSeconds ?: 0}S HOLD"
                                            }
                                            Text(details, fontFamily = FontFamily.Monospace, fontSize = 12.sp, color = MaterialTheme.colorScheme.primary)
                                        }
                                        var expanded by remember { mutableStateOf(false) }
                                        Box {
                                            IconButton(onClick = { expanded = true }) {
                                                Icon(Icons.Default.MoreVert, contentDescription = "More")
                                            }
                                            DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                                                DropdownMenuItem(text = { Text("Edit") }, onClick = { expanded = false; editingExercise = Pair(session.id, ex) })
                                                DropdownMenuItem(text = { Text("Delete", color = MaterialTheme.colorScheme.error) }, onClick = { expanded = false; viewModel.deleteExercise(entity, session.id, ex.id) })
                                            }
                                        }
                                    }"""
row_new = """                                    Row(
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .combinedClickable(
                                                onClick = {},
                                                onLongClick = { editingExercise = Pair(session.id, ex) }
                                            )
                                            .padding(vertical = 4.dp),
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Column(modifier = Modifier.weight(1f)) {
                                            Text("> ${ex.name.uppercase(Locale.getDefault())}", fontFamily = FontFamily.Monospace, fontWeight = FontWeight.Bold)
                                            val details = when (ex.type) {
                                                ExerciseType.REPS_ONLY -> "${ex.sets.size} SETS"
                                                ExerciseType.TIMED_DISTANCE -> "${ex.distanceMeters ?: 0}M IN ${ex.durationSeconds ?: 0}S"
                                                ExerciseType.STATIC_HOLD -> "${ex.durationSeconds ?: 0}S HOLD"
                                            }
                                            Text(details, fontFamily = FontFamily.Monospace, fontSize = 12.sp, color = MaterialTheme.colorScheme.primary)
                                        }
                                    }"""
content = content.replace(row_old, row_new)

# 2. Update GymExerciseSheet signature and calls
content = content.replace("onSave: (ExerciseLog) -> Unit", "onSave: (String, ExerciseType, ExerciseSet?, Int?, Int?) -> Unit,\n    onDelete: (() -> Unit)? = null")

content = content.replace("""        addingExerciseToSession?.let { sessionId ->
            GymExerciseSheet(
                historicalExercises = historicalExercises,
                initialExercise = null,
                onDismiss = { addingExerciseToSession = null },
                onSave = { ex ->
                    val payload = viewModel.getParsedPayload(entity) as? GymPayload ?: return@GymExerciseSheet
                    val updatedRoutines = payload.routines.map { s -> if (s.id == sessionId) s.copy(exercises = s.exercises + ex) else s }
                    viewModel.updateGymPayload(entity, payload.copy(routines = updatedRoutines))
                    addingExerciseToSession = null
                }
            )
        }""", """        addingExerciseToSession?.let { sessionId ->
            GymExerciseSheet(
                historicalExercises = historicalExercises,
                initialExercise = null,
                onDismiss = { addingExerciseToSession = null },
                onSave = { exName, type, newSet, dur, dist ->
                    viewModel.logGymSet(entity, sessionId, exName, type, newSet, dur, dist)
                    addingExerciseToSession = null
                }
            )
        }""")

content = content.replace("""        editingExercise?.let { (sessionId, ex) ->
            GymExerciseSheet(
                historicalExercises = historicalExercises,
                initialExercise = ex,
                onDismiss = { editingExercise = null },
                onSave = { updatedEx ->
                    viewModel.updateExercise(entity, sessionId, updatedEx)
                    editingExercise = null
                }
            )
        }""", """        editingExercise?.let { (sessionId, ex) ->
            GymExerciseSheet(
                historicalExercises = historicalExercises,
                initialExercise = ex,
                onDismiss = { editingExercise = null },
                onSave = { exName, type, newSet, dur, dist ->
                    viewModel.logGymSet(entity, sessionId, exName, type, newSet, dur, dist)
                    editingExercise = null
                },
                onDelete = {
                    viewModel.deleteExercise(entity, sessionId, ex.id)
                    editingExercise = null
                }
            )
        }""")

# 3. Update the DONE button logic in GymExerciseSheet
done_old = """                            if (key == "DONE") {
                                if (name.isNotBlank()) {
                                    val sets = if (type == ExerciseType.REPS_ONLY) {
                                        listOf(ExerciseSet(
                                            id = initialExercise?.sets?.firstOrNull()?.id ?: UUID.randomUUID().toString(),
                                            reps = repsStr.toIntOrNull() ?: 0,
                                            weightKg = weightStr.toFloatOrNull()
                                        ))
                                    } else {
                                        emptyList()
                                    }
                                    val ex = ExerciseLog(
                                        id = initialExercise?.id ?: UUID.randomUUID().toString(),
                                        name = name,
                                        type = type,
                                        sets = sets,
                                        distanceMeters = if (type == ExerciseType.TIMED_DISTANCE) distanceStr.toIntOrNull() else null,
                                        durationSeconds = if (type == ExerciseType.TIMED_DISTANCE || type == ExerciseType.STATIC_HOLD) durationStr.toIntOrNull() else null
                                    )
                                    onSave(ex)
                                }
                            }"""
done_new = """                            if (key == "DONE") {
                                if (name.isNotBlank()) {
                                    val newSet = if (type == ExerciseType.REPS_ONLY) {
                                        ExerciseSet(
                                            id = UUID.randomUUID().toString(),
                                            reps = repsStr.toIntOrNull() ?: 0,
                                            weightKg = weightStr.toFloatOrNull()
                                        )
                                    } else null
                                    
                                    val dist = if (type == ExerciseType.TIMED_DISTANCE) distanceStr.toIntOrNull() else null
                                    val dur = if (type == ExerciseType.TIMED_DISTANCE || type == ExerciseType.STATIC_HOLD) durationStr.toIntOrNull() else null
                                    
                                    onSave(name, type, newSet, dur, dist)
                                }
                            }"""
content = content.replace(done_old, done_new)

# Add delete button if onDelete is provided
# We will append it below the LazyVerticalGrid
grid_end = "            }\n        }\n    }\n}"
delete_button = """            }
            if (onDelete != null) {
                OutlinedButton(
                    onClick = onDelete,
                    modifier = Modifier.fillMaxWidth(),
                    shape = RectangleShape
                ) {
                    Text("DELETE EXERCISE", color = MaterialTheme.colorScheme.error)
                }
            }
        }
    }
}"""
content = content.replace(grid_end, delete_button)

with open("app/src/main/java/com/example/ui/screens/GymTrackerUI.kt", "w") as f:
    f.write(content)
