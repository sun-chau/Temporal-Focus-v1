package com.example.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.*
import com.google.gson.Gson
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class TrackerViewModel(application: Application) : AndroidViewModel(application) {
    private val trackerDao = AppDatabase.getDatabase(application).trackerDao()
    private val gson = Gson()
    val trackers: StateFlow<List<TrackerEntity>> = trackerDao.getAllTrackers().stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
    
    fun getParsedPayload(entity: TrackerEntity): Any? {
        return try {
            val json = if (entity.payloadData.isBlank() || entity.payloadData == "{}") null else entity.payloadData
            when (entity.type) {
                TrackerType.GYM -> json?.let { gson.fromJson(it, GymPayload::class.java) } ?: GymPayload()
                TrackerType.SYLLABUS -> json?.let { gson.fromJson(it, SyllabusPayload::class.java) } ?: SyllabusPayload()
                TrackerType.CUSTOM -> json?.let { gson.fromJson(it, CustomPayload::class.java) } ?: CustomPayload()
                TrackerType.ASSIGNMENT -> json?.let { gson.fromJson(it, AssignmentPayload::class.java) } ?: AssignmentPayload()
            }
        } catch (e: Exception) {
            null
        }
    }

    fun updateGymPayload(entity: TrackerEntity, payload: GymPayload) {
        val newData = gson.toJson(payload)
        updateTracker(entity.copy(payloadData = newData, lastModified = System.currentTimeMillis()))
    }

    fun updateSyllabusPayload(entity: TrackerEntity, payload: SyllabusPayload) {
        val newData = gson.toJson(payload)
        updateTracker(entity.copy(payloadData = newData, lastModified = System.currentTimeMillis()))
    }

    fun updateCustomPayload(entity: TrackerEntity, payload: CustomPayload) {
        val newData = gson.toJson(payload)
        updateTracker(entity.copy(payloadData = newData, lastModified = System.currentTimeMillis()))
    }

    fun updateAssignmentPayload(entity: TrackerEntity, payload: AssignmentPayload) {
        val newData = gson.toJson(payload)
        updateTracker(entity.copy(payloadData = newData, lastModified = System.currentTimeMillis()))
    }


    fun getTrackerById(id: String) = trackerDao.getTrackerById(id)

    fun deleteExercise(tracker: TrackerEntity, sessionId: String, exerciseId: String) {
        val payload = getParsedPayload(tracker) as? GymPayload ?: return
        val updatedRoutines = payload.routines.map { session ->
            if (session.id == sessionId) {
                session.copy(exercises = session.exercises.filter { it.id != exerciseId })
            } else {
                session
            }
        }
        updateGymPayload(tracker, payload.copy(routines = updatedRoutines))
    }

    fun updateExercise(tracker: TrackerEntity, sessionId: String, updatedExercise: ExerciseLog) {
        val payload = getParsedPayload(tracker) as? GymPayload ?: return
        val updatedRoutines = payload.routines.map { session ->
            if (session.id == sessionId) {
                session.copy(exercises = session.exercises.map { if (it.id == updatedExercise.id) updatedExercise else it })
            } else {
                session
            }
        }
        updateGymPayload(tracker, payload.copy(routines = updatedRoutines))
    }


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


    // Custom Tracker Mutations
    fun deleteCustomEntry(tracker: TrackerEntity, entryId: String) {
        val payload = getParsedPayload(tracker) as? CustomPayload ?: return
        val newEntries = payload.entries.filter { it.id != entryId }
        updateCustomPayload(tracker, payload.copy(entries = newEntries))
    }

    fun updateCustomEntry(tracker: TrackerEntity, entryId: String, newFieldData: Map<String, String>) {
        val payload = getParsedPayload(tracker) as? CustomPayload ?: return
        val newEntries = payload.entries.map {
            if (it.id == entryId) it.copy(fieldData = newFieldData) else it
        }
        updateCustomPayload(tracker, payload.copy(entries = newEntries))
    }


    fun addCustomEntry(tracker: TrackerEntity, fieldData: Map<String, String>) {
        val payload = getParsedPayload(tracker) as? CustomPayload ?: return
        val newEntry = CustomEntry(
            timestampEpoch = System.currentTimeMillis(),
            fieldData = fieldData
        )
        updateCustomPayload(tracker, payload.copy(entries = payload.entries + newEntry))
    }

    fun insertTracker(tracker: TrackerEntity) {
        viewModelScope.launch(Dispatchers.IO) {
            trackerDao.insertTracker(tracker)
        }
    }

    fun updateTracker(tracker: TrackerEntity) {
        viewModelScope.launch(Dispatchers.IO) {
            trackerDao.updateTracker(tracker)
        }
    }

    fun deleteTracker(tracker: TrackerEntity) {
        viewModelScope.launch(Dispatchers.IO) {
            trackerDao.deleteTracker(tracker)
        }
    }
}
