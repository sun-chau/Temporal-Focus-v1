import re
with open("app/src/main/java/com/example/viewmodel/TrackerViewModel.kt", "r") as f:
    content = f.read()

new_methods = """
    fun getTelemetryString(entity: TrackerEntity): String {
        return try {
            val payload = getParsedPayload(entity)
            when (entity.type) {
                TrackerType.ASSIGNMENT -> {
                    val p = payload as? AssignmentPayload ?: AssignmentPayload()
                    val pending = p.tasks.count { it.status == AssignmentStatus.PENDING }
                    val active = p.tasks.count { it.status == AssignmentStatus.IN_PROGRESS }
                    val submitted = p.tasks.count { it.status == AssignmentStatus.SUBMITTED }
                    "[ $pending PENDING | $active ACTIVE | $submitted SUBMITTED ]"
                }
                TrackerType.SYLLABUS -> {
                    val p = payload as? SyllabusPayload ?: SyllabusPayload()
                    val allSubTopics = p.subjects.flatMap { it.modules }.flatMap { it.subTopics }
                    val completed = allSubTopics.count { it.isCompleted }
                    val total = allSubTopics.size
                    "[ $completed / $total TOPICS COMPLETED ]"
                }
                TrackerType.GYM -> {
                    val p = payload as? GymPayload ?: GymPayload()
                    "[ ${p.routines.size} SESSIONS LOGGED ]"
                }
                TrackerType.CUSTOM -> {
                    "[ CUSTOM TRACKER ]"
                }
            }
        } catch (e: Exception) {
            "[ ERROR ]"
        }
    }

    // Assignments Mutations
    fun deleteAssignment(tracker: TrackerEntity, assignmentId: String) {
        val payload = getParsedPayload(tracker) as? AssignmentPayload ?: return
        val newTasks = payload.tasks.filter { it.id != assignmentId }
        updateAssignmentPayload(tracker, payload.copy(tasks = newTasks))
    }

    fun updateAssignment(tracker: TrackerEntity, assignmentId: String, newTitle: String, newPriority: PriorityLevel) {
        val payload = getParsedPayload(tracker) as? AssignmentPayload ?: return
        val newTasks = payload.tasks.map { 
            if (it.id == assignmentId) it.copy(title = newTitle, priority = newPriority) else it
        }
        updateAssignmentPayload(tracker, payload.copy(tasks = newTasks))
    }

    fun updateAssignmentPriority(tracker: TrackerEntity, assignmentId: String, priority: PriorityLevel) {
        val payload = getParsedPayload(tracker) as? AssignmentPayload ?: return
        val newTasks = payload.tasks.map { 
            if (it.id == assignmentId) it.copy(priority = priority) else it
        }
        updateAssignmentPayload(tracker, payload.copy(tasks = newTasks))
    }

    // Syllabus Mutations
    fun deleteSubject(tracker: TrackerEntity, subjectId: String) {
        val payload = getParsedPayload(tracker) as? SyllabusPayload ?: return
        updateSyllabusPayload(tracker, payload.copy(subjects = payload.subjects.filter { it.id != subjectId }))
    }

    fun updateSubject(tracker: TrackerEntity, subjectId: String, newTitle: String, newPriority: PriorityLevel) {
        val payload = getParsedPayload(tracker) as? SyllabusPayload ?: return
        val newSubjects = payload.subjects.map {
            if (it.id == subjectId) it.copy(name = newTitle, priority = newPriority) else it
        }
        updateSyllabusPayload(tracker, payload.copy(subjects = newSubjects))
    }

    fun deleteModule(tracker: TrackerEntity, subjectId: String, moduleId: String) {
        val payload = getParsedPayload(tracker) as? SyllabusPayload ?: return
        val newSubjects = payload.subjects.map { sub ->
            if (sub.id == subjectId) sub.copy(modules = sub.modules.filter { it.id != moduleId }) else sub
        }
        updateSyllabusPayload(tracker, payload.copy(subjects = newSubjects))
    }

    fun updateModule(tracker: TrackerEntity, subjectId: String, moduleId: String, newTitle: String) {
        val payload = getParsedPayload(tracker) as? SyllabusPayload ?: return
        val newSubjects = payload.subjects.map { sub ->
            if (sub.id == subjectId) {
                sub.copy(modules = sub.modules.map { mod -> 
                    if (mod.id == moduleId) mod.copy(title = newTitle) else mod
                })
            } else sub
        }
        updateSyllabusPayload(tracker, payload.copy(subjects = newSubjects))
    }

    fun deleteSubTopic(tracker: TrackerEntity, subjectId: String, moduleId: String, subTopicId: String) {
        val payload = getParsedPayload(tracker) as? SyllabusPayload ?: return
        val newSubjects = payload.subjects.map { sub ->
            if (sub.id == subjectId) {
                sub.copy(modules = sub.modules.map { mod ->
                    if (mod.id == moduleId) {
                        mod.copy(subTopics = mod.subTopics.filter { it.id != subTopicId })
                    } else mod
                })
            } else sub
        }
        updateSyllabusPayload(tracker, payload.copy(subjects = newSubjects))
    }

    fun updateSubTopic(tracker: TrackerEntity, subjectId: String, moduleId: String, subTopicId: String, newTitle: String, isCompleted: Boolean) {
        val payload = getParsedPayload(tracker) as? SyllabusPayload ?: return
        val newSubjects = payload.subjects.map { sub ->
            if (sub.id == subjectId) {
                sub.copy(modules = sub.modules.map { mod ->
                    if (mod.id == moduleId) {
                        mod.copy(subTopics = mod.subTopics.map { st -> 
                            if (st.id == subTopicId) st.copy(title = newTitle, isCompleted = isCompleted) else st
                        })
                    } else mod
                })
            } else sub
        }
        updateSyllabusPayload(tracker, payload.copy(subjects = newSubjects))
    }

    fun insertTracker"""

content = content.replace("    fun insertTracker", new_methods)

with open("app/src/main/java/com/example/viewmodel/TrackerViewModel.kt", "w") as f:
    f.write(content)
