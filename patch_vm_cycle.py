import re

with open("app/src/main/java/com/example/viewmodel/TrackerViewModel.kt", "r") as f:
    content = f.read()

cycle_func = """
    fun cycleAssignmentStatus(tracker: TrackerEntity, taskId: String) {
        val payload = getParsedPayload(tracker) as? AssignmentPayload ?: return
        val task = payload.tasks.find { it.id == taskId } ?: return
        
        val newStatus = when (task.status) {
            AssignmentStatus.PENDING -> AssignmentStatus.IN_PROGRESS
            AssignmentStatus.IN_PROGRESS -> AssignmentStatus.SUBMITTED
            AssignmentStatus.SUBMITTED -> AssignmentStatus.PENDING
        }
        
        var newTasks = payload.tasks.map { if (it.id == taskId) it.copy(status = newStatus) else it }
        
        if (newStatus == AssignmentStatus.SUBMITTED && task.recurrence == Recurrence.WEEKLY) {
            val newWeeklyTask = Deliverable(
                title = task.title,
                status = AssignmentStatus.PENDING,
                deadlineEpoch = task.deadlineEpoch + 604800000L,
                priority = task.priority,
                recurrence = Recurrence.WEEKLY
            )
            newTasks = newTasks + newWeeklyTask
        }
        
        updateAssignmentPayload(tracker, payload.copy(tasks = newTasks))
    }
"""

if "fun cycleAssignmentStatus" not in content:
    content = content.replace("    fun updateAssignmentPriority", cycle_func + "    fun updateAssignmentPriority")

with open("app/src/main/java/com/example/viewmodel/TrackerViewModel.kt", "w") as f:
    f.write(content)

