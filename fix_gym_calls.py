with open("app/src/main/java/com/example/ui/screens/GymTrackerUI.kt", "r") as f:
    content = f.read()

import re

# Fix adding
add_old = """    if (addingToSessionId != null) {
        GymExerciseSheet(
            historicalExercises = historicalExercises,
            initialExercise = null,
            onDismiss = { addingToSessionId = null },
            onSave = { newEx ->
                val newRoutines = payload.routines.map { s ->
                    if (s.id == addingToSessionId) s.copy(exercises = s.exercises + newEx) else s
                }
                viewModel.updateGymPayload(entity, payload.copy(routines = newRoutines))
                addingToSessionId = null
            }
        )
    }"""
add_new = """    if (addingToSessionId != null) {
        GymExerciseSheet(
            historicalExercises = historicalExercises,
            initialExercise = null,
            onDismiss = { addingToSessionId = null },
            onSave = { exName, type, newSet, dur, dist ->
                addingToSessionId?.let { sessionId ->
                    viewModel.logGymSet(entity, sessionId, exName, type, newSet, dur, dist)
                }
                addingToSessionId = null
            }
        )
    }"""
content = content.replace(add_old, add_new)

# Fix editing
edit_old = """    editingExercise?.let { (sessionId, ex) ->
        GymExerciseSheet(
            historicalExercises = historicalExercises,
            initialExercise = ex,
            onDismiss = { editingExercise = null },
            onSave = { updatedEx ->
                viewModel.updateExercise(entity, sessionId, updatedEx)
                editingExercise = null
            }
        )
    }"""
edit_new = """    editingExercise?.let { (sessionId, ex) ->
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
    }"""
content = content.replace(edit_old, edit_new)

# Fix the DONE button logic
done_old = r"""                            if \(key == "DONE"\) \{
                                if \(name.isNotBlank\(\)\) \{
                                    val sets = if \(type == ExerciseType.REPS_ONLY\) \{
                                        listOf\(ExerciseSet\(
                                            id = initialExercise\?\.sets\?\.firstOrNull\(\)\?\.id \?: UUID.randomUUID\(\)\.toString\(\),
                                            reps = repsStr.toIntOrNull\(\) \?: 0,
                                            weightKg = weightStr.toFloatOrNull\(\)
                                        \)\)
                                    \} else \{
                                        emptyList\(\)
                                    \}
                                    val ex = ExerciseLog\(
                                        id = initialExercise\?\.id \?: UUID.randomUUID\(\)\.toString\(\),
                                        name = name,
                                        type = type,
                                        sets = sets,
                                        distanceMeters = if \(type == ExerciseType.TIMED_DISTANCE\) distanceStr.toIntOrNull\(\) else null,
                                        durationSeconds = if \(type == ExerciseType.TIMED_DISTANCE \|\| type == ExerciseType.STATIC_HOLD\) durationStr.toIntOrNull\(\) else null
                                    \)
                                    onSave\(ex\)
                                \}
                            \}"""

done_new = """                            if (key == "DONE") {
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
                            }"""
content = re.sub(done_old, done_new, content, flags=re.MULTILINE)


with open("app/src/main/java/com/example/ui/screens/GymTrackerUI.kt", "w") as f:
    f.write(content)

