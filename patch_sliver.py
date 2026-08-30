import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

target = """                            val actualStart = maxOf(startOfDay, effectiveStartTime)
                            val actualEnd = minOf(endOfDay + 1, effectiveEndTime)
                            
                            val startCal = Calendar.getInstance().apply { timeInMillis = actualStart }
                            val startMinutes = if (effectiveStartTime < startOfDay) 0 else startCal.get(Calendar.HOUR_OF_DAY) * 60 + startCal.get(Calendar.MINUTE)
                            
                            val endMinutes = if (effectiveEndTime > endOfDay) 24 * 60 else {
                                val endCal = Calendar.getInstance().apply { timeInMillis = actualEnd }
                                endCal.get(Calendar.HOUR_OF_DAY) * 60 + endCal.get(Calendar.MINUTE)
                            }
                            
                            val durationMinutes = maxOf(10, endMinutes - startMinutes)"""

replacement = """                            val actualStart = if (isDragging) effectiveStartTime else maxOf(startOfDay, effectiveStartTime)
                            val actualEnd = if (isDragging) effectiveEndTime else minOf(endOfDay + 1, effectiveEndTime)
                            
                            val startMinutes = if (isDragging) {
                                ((effectiveStartTime - startOfDay) / 60000L).toInt()
                            } else {
                                val startCal = Calendar.getInstance().apply { timeInMillis = actualStart }
                                if (effectiveStartTime < startOfDay) 0 else startCal.get(Calendar.HOUR_OF_DAY) * 60 + startCal.get(Calendar.MINUTE)
                            }
                            
                            val endMinutes = if (isDragging) {
                                ((effectiveEndTime - startOfDay) / 60000L).toInt()
                            } else {
                                if (effectiveEndTime > endOfDay) 24 * 60 else {
                                    val endCal = Calendar.getInstance().apply { timeInMillis = actualEnd }
                                    endCal.get(Calendar.HOUR_OF_DAY) * 60 + endCal.get(Calendar.MINUTE)
                                }
                            }
                            
                            val durationMinutes = maxOf(10, endMinutes - startMinutes)"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
