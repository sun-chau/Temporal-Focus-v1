with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

content = content.replace("val dayOfMonth = cal.get(Calendar.DAY_OF_MONTH).toString()", """val dayOfMonth = cal.get(Calendar.DAY_OF_MONTH).toString()
            val monthStr = when (cal.get(Calendar.MONTH)) {
                java.util.Calendar.JANUARY -> "Jan"
                java.util.Calendar.FEBRUARY -> "Feb"
                java.util.Calendar.MARCH -> "Mar"
                java.util.Calendar.APRIL -> "Apr"
                java.util.Calendar.MAY -> "May"
                java.util.Calendar.JUNE -> "Jun"
                java.util.Calendar.JULY -> "Jul"
                java.util.Calendar.AUGUST -> "Aug"
                java.util.Calendar.SEPTEMBER -> "Sep"
                java.util.Calendar.OCTOBER -> "Oct"
                java.util.Calendar.NOVEMBER -> "Nov"
                java.util.Calendar.DECEMBER -> "Dec"
                else -> ""
            }""")

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
