with open("app/src/main/java/com/example/data/TrackerEntity.kt", "r") as f:
    content = f.read()

import re

# Update SyllabusPayload and Subject
new_syllabus = """enum class PriorityLevel { LOW, MID, CRITICAL }

data class SyllabusPayload(val subjects: List<Subject> = emptyList())
data class Subject(val id: String = UUID.randomUUID().toString(), val name: String, val priority: PriorityLevel = PriorityLevel.MID, val modules: List<Module> = emptyList())
data class Module(val id: String = UUID.randomUUID().toString(), val title: String, val weightage: Int, val subTopics: List<SubTopic> = emptyList())
data class SubTopic(val id: String = UUID.randomUUID().toString(), val title: String, val isCompleted: Boolean = false)
"""

content = re.sub(r'data class SyllabusPayload.*?data class Subject\([^)]+\)', new_syllabus, content, flags=re.DOTALL)

# Add priority to Deliverable
content = re.sub(
    r'val status: AssignmentStatus = AssignmentStatus\.PENDING,\s*val deadlineEpoch: Long',
    'val status: AssignmentStatus = AssignmentStatus.PENDING,\n    val deadlineEpoch: Long,\n    val priority: PriorityLevel = PriorityLevel.MID',
    content
)

with open("app/src/main/java/com/example/data/TrackerEntity.kt", "w") as f:
    f.write(content)
