import re

with open("app/src/main/java/com/example/ui/screens/GymTrackerUI.kt", "r") as f:
    content = f.read()

# Calculate hasChanges
# For Edit Modals: Compare the current mutable state variables to the original object's properties.
# For Add Modals: Check if the mandatory input fields are no longer in their default, empty state.

has_changes_logic = """
            val hasChanges = if (initialExercise != null) {
                name != initialExercise.name || type != initialExercise.type ||
                repsStr != (initialExercise.sets.firstOrNull()?.reps?.toString() ?: "") ||
                weightStr != (initialExercise.sets.firstOrNull()?.weightKg?.toString() ?: "") ||
                distanceStr != (initialExercise.distanceMeters?.toString() ?: "") ||
                durationStr != (initialExercise.durationSeconds?.toString() ?: "")
            } else {
                name.isNotBlank()
            }
"""

numpad_old = """            val keys = listOf("1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "0", "DEL", "DONE")
            LazyVerticalGrid(
                columns = GridCells.Fixed(3),
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(keys) { key ->
                    Button(
                        onClick = {
                            if (key == "DONE") {
                                if (name.isNotBlank()) {
                                    val newSet = if (type == ExerciseType.REPS_ONLY) {
                                        ExerciseSet(
                                            id = initialExercise?.sets?.firstOrNull()?.id ?: UUID.randomUUID().toString(),
                                            reps = repsStr.toIntOrNull() ?: 0,
                                            weightKg = weightStr.toFloatOrNull()
                                        )
                                    } else null
                                    
                                    val dist = if (type == ExerciseType.TIMED_DISTANCE) distanceStr.toIntOrNull() else null
                                    val dur = if (type == ExerciseType.TIMED_DISTANCE || type == ExerciseType.STATIC_HOLD) durationStr.toIntOrNull() else null
                                    
                                    onSave(name, type, newSet, dur, dist)
                                }
                            } else if (key == "DEL") {
                                when (activeField) {
                                    "REPS" -> if (repsStr.isNotEmpty()) repsStr = repsStr.dropLast(1)
                                    "WEIGHT" -> if (weightStr.isNotEmpty()) weightStr = weightStr.dropLast(1)
                                    "DISTANCE" -> if (distanceStr.isNotEmpty()) distanceStr = distanceStr.dropLast(1)
                                    "DURATION" -> if (durationStr.isNotEmpty()) durationStr = durationStr.dropLast(1)
                                }
                            } else {
                                when (activeField) {
                                    "REPS" -> repsStr += key
                                    "WEIGHT" -> weightStr += key
                                    "DISTANCE" -> distanceStr += key
                                    "DURATION" -> durationStr += key
                                }
                            }
                        },
                        modifier = Modifier.aspectRatio(if (key == "DONE") 3f else 2f),
                        shape = RectangleShape,
                        colors = if (key == "DONE") ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary) else ButtonDefaults.filledTonalButtonColors()
                    ) {
                        Text(key, fontWeight = FontWeight.Bold, fontSize = 20.sp)
                    }
                }
            }"""

numpad_new = has_changes_logic + """            val keys = listOf("1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "0", "DEL")
            LazyVerticalGrid(
                columns = GridCells.Fixed(3),
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(keys) { key ->
                    Button(
                        onClick = {
                            if (key == "DEL") {
                                when (activeField) {
                                    "REPS" -> if (repsStr.isNotEmpty()) repsStr = repsStr.dropLast(1)
                                    "WEIGHT" -> if (weightStr.isNotEmpty()) weightStr = weightStr.dropLast(1)
                                    "DISTANCE" -> if (distanceStr.isNotEmpty()) distanceStr = distanceStr.dropLast(1)
                                    "DURATION" -> if (durationStr.isNotEmpty()) durationStr = durationStr.dropLast(1)
                                }
                            } else {
                                when (activeField) {
                                    "REPS" -> repsStr += key
                                    "WEIGHT" -> weightStr += key
                                    "DISTANCE" -> distanceStr += key
                                    "DURATION" -> durationStr += key
                                }
                            }
                        },
                        modifier = Modifier.aspectRatio(2f),
                        shape = RectangleShape,
                        colors = ButtonDefaults.filledTonalButtonColors()
                    ) {
                        Text(key, fontWeight = FontWeight.Bold, fontSize = 20.sp)
                    }
                }
            }
            Button(
                onClick = {
                    if (name.isNotBlank()) {
                        val newSet = if (type == ExerciseType.REPS_ONLY) {
                            ExerciseSet(
                                id = initialExercise?.sets?.firstOrNull()?.id ?: UUID.randomUUID().toString(),
                                reps = repsStr.toIntOrNull() ?: 0,
                                weightKg = weightStr.toFloatOrNull()
                            )
                        } else null
                        
                        val dist = if (type == ExerciseType.TIMED_DISTANCE) distanceStr.toIntOrNull() else null
                        val dur = if (type == ExerciseType.TIMED_DISTANCE || type == ExerciseType.STATIC_HOLD) durationStr.toIntOrNull() else null
                        
                        onSave(name, type, newSet, dur, dist)
                    }
                },
                modifier = Modifier.fillMaxWidth(),
                shape = RectangleShape,
                enabled = hasChanges,
                colors = ButtonDefaults.buttonColors(
                    disabledContainerColor = MaterialTheme.colorScheme.surfaceVariant,
                    disabledContentColor = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)
                )
            ) {
                Text(if (hasChanges) "SAVE CHANGES" else "NO CHANGES", fontWeight = FontWeight.Bold)
            }"""

content = content.replace(numpad_old, numpad_new)

with open("app/src/main/java/com/example/ui/screens/GymTrackerUI.kt", "w") as f:
    f.write(content)

