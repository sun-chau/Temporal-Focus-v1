package com.example.data

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.util.UUID

enum class TrackerType { GYM, SYLLABUS, ASSIGNMENT, CUSTOM, BINARY, VOLUME, BURN_RATE }

@Entity(tableName = "trackers")
data class TrackerEntity(
    @PrimaryKey val id: String = UUID.randomUUID().toString(),
    val title: String,
    val type: TrackerType,
    val createdAt: Long = System.currentTimeMillis(),
    val lastModified: Long = System.currentTimeMillis(),
    val payloadData: String = "{}"
)

enum class PriorityLevel { LOW, MID, CRITICAL }

data class SyllabusPayload(val subjects: List<Subject> = emptyList())

data class Subject(
    val id: String = UUID.randomUUID().toString(),
    val name: String,
    val priority: PriorityLevel = PriorityLevel.MID,
    val modules: List<Module> = emptyList()
)

data class Module(
    val id: String = UUID.randomUUID().toString(),
    val title: String,
    val weightage: Int,
    val subTopics: List<SubTopic> = emptyList()
)

data class SubTopic(
    val id: String = UUID.randomUUID().toString(),
    val title: String,
    val isCompleted: Boolean = false
)

data class AssignmentPayload(val tasks: List<Deliverable> = emptyList())

data class Deliverable(
    val id: String = UUID.randomUUID().toString(),
    val title: String,
    val status: AssignmentStatus = AssignmentStatus.PENDING,
    val deadlineEpoch: Long,
    val priority: PriorityLevel = PriorityLevel.MID
)

enum class AssignmentStatus { PENDING, IN_PROGRESS, SUBMITTED }

data class ExerciseSet(
    val id: String = UUID.randomUUID().toString(),
    val reps: Int,
    val weightKg: Float? = null
)

data class GymPayload(val routines: List<WorkoutSession> = emptyList())

data class WorkoutSession(
    val id: String = UUID.randomUUID().toString(),
    val dateEpoch: Long,
    val exercises: List<ExerciseLog> = emptyList()
)

data class ExerciseLog(
    val id: String = UUID.randomUUID().toString(),
    val name: String,
    val type: ExerciseType,
    val sets: List<ExerciseSet> = emptyList(),
    val durationSeconds: Int? = null,
    val distanceMeters: Int? = null
)

enum class ExerciseType { REPS_ONLY, TIMED_DISTANCE, STATIC_HOLD }

data class CustomPayload(val schema: List<CustomField> = emptyList(), val entries: List<CustomEntry> = emptyList())
data class CustomEntry(val id: String = UUID.randomUUID().toString(), val timestampEpoch: Long, val fieldData: Map<String, String>)
data class CustomField(val id: String = UUID.randomUUID().toString(), val label: String, val fieldType: CustomFieldType)
enum class CustomFieldType { NUMBER, TEXT, CHECKBOX }


// --- New Schemas ---

data class BinaryPayload(val disciplines: List<BinaryDiscipline> = emptyList())
data class BinaryDiscipline(val id: String, val name: String, val completedDates: Set<String> = emptySet())

data class VolumePayload(val resources: List<VolumeResource> = emptyList())
data class VolumeResource(val id: String, val title: String, val currentProgress: Int, val totalProgress: Int, val metricLabel: String)

data class BurnRatePayload(val monthlyLimit: Double = 0.0, val customTags: Set<String> = emptySet(), val transactions: List<Transaction> = emptyList())
data class Transaction(val id: String, val amount: Double, val timestampEpoch: Long, val tag: String)
