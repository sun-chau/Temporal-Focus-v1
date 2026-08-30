package com.example.data

import java.util.Calendar

enum class MonthlyType { DATES, LAST_DAY, DAY_OF_WEEK }
enum class AnnuallyType { DATES, END_OF_YEAR, DAY_OF_WEEK }

data class DailyScheduleDraft(
    val title: String = "",
    val startTime: Long = System.currentTimeMillis(),
    val endTime: Long = System.currentTimeMillis() + 3600 * 1000,
    val label: String = "",
    
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
    val seriesId: String? = null
)


data class DeadlineDraft(
    val name: String = "",
    val description: String? = null,
    val labels: String = "",
    val targetTime: Long = System.currentTimeMillis() + 86400000L,
    val priority: String = "Normal",
    val deadlineDateTime: Long? = null,
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


data class RecurrencePattern(
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
    val occurrenceCount: Int = 1
) {
    fun generateOccurrences(startTime: Long, maxIterations: Int = 3650): List<Long> {
        if (!isRecurring) return listOf(startTime)
        
        val occurrences = mutableListOf<Long>()
        val cal = Calendar.getInstance().apply { timeInMillis = startTime }
        var count = 0
        val limit = if (occurrenceCount <= 0) Int.MAX_VALUE else occurrenceCount
        var iterations = 0
        
        while (count < limit && iterations < maxIterations) {
            var match = false
            when (recurrenceType) {
                RecurrenceType.DAILY -> {
                    match = (iterations % dailyInterval.coerceIn(1, 120)) == 0
                }
                RecurrenceType.WEEKLY -> {
                    val dayOfWeek = cal.get(Calendar.DAY_OF_WEEK)
                    match = weeklyDays.contains(dayOfWeek)
                }
                RecurrenceType.MONTHLY -> {
                    when (monthlyType) {
                        MonthlyType.DATES -> {
                            val date = cal.get(Calendar.DAY_OF_MONTH)
                            match = monthlyDates.contains(date)
                        }
                        MonthlyType.LAST_DAY -> {
                            val lastDay = cal.getActualMaximum(Calendar.DAY_OF_MONTH)
                            match = cal.get(Calendar.DAY_OF_MONTH) == lastDay
                        }
                        MonthlyType.DAY_OF_WEEK -> {
                            val dayOfWeek = cal.get(Calendar.DAY_OF_WEEK)
                            val weekOfMonth = cal.get(Calendar.DAY_OF_WEEK_IN_MONTH)
                            
                            val targetWeek = if (monthlyWeek == 5) {
                                val tempCal = cal.clone() as Calendar
                                tempCal.set(Calendar.DAY_OF_MONTH, tempCal.getActualMaximum(Calendar.DAY_OF_MONTH))
                                while (tempCal.get(Calendar.DAY_OF_WEEK) != monthlyDayOfWeek) {
                                    tempCal.add(Calendar.DAY_OF_MONTH, -1)
                                }
                                tempCal.get(Calendar.DAY_OF_WEEK_IN_MONTH)
                            } else {
                                monthlyWeek
                            }
                            match = (dayOfWeek == monthlyDayOfWeek && weekOfMonth == targetWeek)
                        }
                    }
                }
                RecurrenceType.ANNUALLY -> {
                    if (cal.get(Calendar.MONTH) == annuallyMonth) {
                        when (annuallyType) {
                            AnnuallyType.DATES -> {
                                val date = cal.get(Calendar.DAY_OF_MONTH)
                                match = annuallyDates.contains(date)
                            }
                            AnnuallyType.END_OF_YEAR -> {
                                val lastDay = cal.getActualMaximum(Calendar.DAY_OF_MONTH)
                                match = cal.get(Calendar.DAY_OF_MONTH) == lastDay
                            }
                            AnnuallyType.DAY_OF_WEEK -> {
                                val dayOfWeek = cal.get(Calendar.DAY_OF_WEEK)
                                val weekOfMonth = cal.get(Calendar.DAY_OF_WEEK_IN_MONTH)
                                
                                val targetWeek = if (annuallyWeek == 5) {
                                    val tempCal = cal.clone() as Calendar
                                    tempCal.set(Calendar.DAY_OF_MONTH, tempCal.getActualMaximum(Calendar.DAY_OF_MONTH))
                                    while (tempCal.get(Calendar.DAY_OF_WEEK) != annuallyDayOfWeek) {
                                        tempCal.add(Calendar.DAY_OF_MONTH, -1)
                                    }
                                    tempCal.get(Calendar.DAY_OF_WEEK_IN_MONTH)
                                } else {
                                    annuallyWeek
                                }
                                match = (dayOfWeek == annuallyDayOfWeek && weekOfMonth == targetWeek)
                            }
                        }
                    }
                }
                else -> {}
            }
            if (match) {
                occurrences.add(cal.timeInMillis)
                count++
            }
            cal.add(Calendar.DAY_OF_YEAR, 1)
            iterations++
        }
        return occurrences
    }
}

fun DailyScheduleDraft.toRecurrencePattern() = RecurrencePattern(
    isRecurring = isRecurring,
    recurrenceType = recurrenceType,
    dailyInterval = dailyInterval,
    weeklyDays = weeklyDays,
    monthlyType = monthlyType,
    monthlyDates = monthlyDates,
    monthlyWeek = monthlyWeek,
    monthlyDayOfWeek = monthlyDayOfWeek,
    annuallyType = annuallyType,
    annuallyMonth = annuallyMonth,
    annuallyDates = annuallyDates,
    annuallyWeek = annuallyWeek,
    annuallyDayOfWeek = annuallyDayOfWeek,
    occurrenceCount = occurrenceCount
)

fun DeadlineDraft.toRecurrencePattern() = RecurrencePattern(
    isRecurring = isRecurring,
    recurrenceType = recurrenceType,
    dailyInterval = dailyInterval,
    weeklyDays = weeklyDays,
    monthlyType = monthlyType,
    monthlyDates = monthlyDates,
    monthlyWeek = monthlyWeek,
    monthlyDayOfWeek = monthlyDayOfWeek,
    annuallyType = annuallyType,
    annuallyMonth = annuallyMonth,
    annuallyDates = annuallyDates,
    annuallyWeek = annuallyWeek,
    annuallyDayOfWeek = annuallyDayOfWeek,
    occurrenceCount = occurrenceCount
)
