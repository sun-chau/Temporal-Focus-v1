import re

with open("app/src/main/java/com/example/data/Recurrence.kt", "r") as f:
    content = f.read()

deadline_draft = """

data class DeadlineDraft(
    val name: String = "",
    val description: String? = null,
    val tags: String = "",
    val targetTime: Long = System.currentTimeMillis() + 86400000L,
    val priority: String = "Normal",
    val reminderDateTime: Long? = null,
    val link: String? = null,
    val attachmentUri: String? = null,
    
    val isRecurring: Boolean = false,
    val recurrenceType: RecurrenceType = RecurrenceType.DAILY,
    
    val dailyInterval: Int = 1,
    val weeklyDays: Set<Int> = emptySet(),
    val monthlyType: MonthlyType = MonthlyType.DATES,
    val monthlyDates: Set<Int> = emptySet(),
    val monthlyWeek: Int = 1,
    val monthlyDayOfWeek: Int = Calendar.SUNDAY,
    val annuallyType: AnnuallyType = AnnuallyType.DATES,
    val annuallyMonth: Int = Calendar.JANUARY,
    val annuallyDates: Set<Int> = emptySet(),
    val annuallyWeek: Int = 1,
    val annuallyDayOfWeek: Int = Calendar.SUNDAY,
    
    val occurrenceCount: Int = 1,
    val editingId: String? = null,
    val createdAt: Long = System.currentTimeMillis()
)
"""

content += deadline_draft

with open("app/src/main/java/com/example/data/Recurrence.kt", "w") as f:
    f.write(content)
