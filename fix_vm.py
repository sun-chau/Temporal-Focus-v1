import re
with open("app/src/main/java/com/example/viewmodel/TrackerViewModel.kt", "r") as f:
    content = f.read()

new_parsed = """    fun getParsedPayload(entity: TrackerEntity): Any? {
        return try {
            val json = if (entity.payloadData.isBlank() || entity.payloadData == "{}") null else entity.payloadData
            when (entity.type) {
                TrackerType.GYM -> {
                    val p = json?.let { gson.fromJson(it, GymPayload::class.java) } ?: GymPayload()
                    p.copy(routines = p.routines ?: emptyList())
                }
                TrackerType.SYLLABUS -> {
                    val p = json?.let { gson.fromJson(it, SyllabusPayload::class.java) } ?: SyllabusPayload()
                    p.copy(subjects = p.subjects ?: emptyList())
                }
                TrackerType.CUSTOM -> {
                    val p = json?.let { gson.fromJson(it, CustomPayload::class.java) } ?: CustomPayload()
                    p.copy(schema = p.schema ?: emptyList(), entries = p.entries ?: emptyList())
                }
                TrackerType.ASSIGNMENT -> {
                    val p = json?.let { gson.fromJson(it, AssignmentPayload::class.java) } ?: AssignmentPayload()
                    p.copy(tasks = p.tasks ?: emptyList())
                }
            }
        } catch (e: Exception) {
            null
        }
    }"""

content = re.sub(r'    fun getParsedPayload.*?    }', new_parsed, content, flags=re.DOTALL)

log_gym_set = """    fun logGymSet(tracker: TrackerEntity, sessionId: String, exerciseName: String, type: ExerciseType, newSet: ExerciseSet?, duration: Int?, distance: Int?) {
        val payload = getParsedPayload(tracker) as? GymPayload ?: return
        val updatedRoutines = payload.routines.map { session ->
            if (session.id == sessionId) {
                val existingExercise = session.exercises.find { it.name == exerciseName }
                if (existingExercise != null) {
                    val updatedExercises = session.exercises.map {
                        if (it.name == exerciseName) {
                            it.copy(
                                sets = if (newSet != null) (it.sets ?: emptyList()) + newSet else (it.sets ?: emptyList()),
                                durationSeconds = duration ?: it.durationSeconds,
                                distanceMeters = distance ?: it.distanceMeters
                            )
                        } else it
                    }
                    session.copy(exercises = updatedExercises)
                } else {
                    val newExercise = ExerciseLog(
                        name = exerciseName,
                        type = type,
                        sets = if (newSet != null) listOf(newSet) else emptyList(),
                        durationSeconds = duration,
                        distanceMeters = distance
                    )
                    session.copy(exercises = (session.exercises ?: emptyList()) + newExercise)
                }
            } else {
                session
            }
        }
        updateGymPayload(tracker, payload.copy(routines = updatedRoutines))
    }

    fun updateGymPayload"""

content = content.replace("    fun updateGymPayload", log_gym_set)

with open("app/src/main/java/com/example/viewmodel/TrackerViewModel.kt", "w") as f:
    f.write(content)
