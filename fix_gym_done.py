with open("app/src/main/java/com/example/ui/screens/GymTrackerUI.kt", "r") as f:
    content = f.read()

import re

# We will just replace everything between 'if (key == "DONE") {' and '} else if (key == "DEL") {'
start_marker = 'if (key == "DONE") {'
end_marker = '} else if (key == "DEL") {'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_logic = """if (key == "DONE") {
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
                            """
    content = content[:start_idx] + new_logic + content[end_idx:]

with open("app/src/main/java/com/example/ui/screens/GymTrackerUI.kt", "w") as f:
    f.write(content)
