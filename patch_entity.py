import re

with open("app/src/main/java/com/example/data/TrackerEntity.kt", "r") as f:
    content = f.read()

recurrence_enum = "enum class Recurrence { NONE, WEEKLY }\n"

if "enum class Recurrence" not in content:
    content = content.replace("enum class AssignmentStatus { PENDING, IN_PROGRESS, SUBMITTED }", 
                              recurrence_enum + "enum class AssignmentStatus { PENDING, IN_PROGRESS, SUBMITTED }")

deliverable_old = """data class Deliverable(
    val id: String = UUID.randomUUID().toString(),
    val title: String,
    val status: AssignmentStatus = AssignmentStatus.PENDING,
    val deadlineEpoch: Long,
    val priority: PriorityLevel = PriorityLevel.MID
)"""

deliverable_new = """data class Deliverable(
    val id: String = UUID.randomUUID().toString(),
    val title: String,
    val status: AssignmentStatus = AssignmentStatus.PENDING,
    val deadlineEpoch: Long,
    val priority: PriorityLevel = PriorityLevel.MID,
    val recurrence: Recurrence = Recurrence.NONE
)"""

content = content.replace(deliverable_old, deliverable_new)

with open("app/src/main/java/com/example/data/TrackerEntity.kt", "w") as f:
    f.write(content)

