import java.util.Calendar

fun main() {
    fun getVisualBounds(startTime: Long, endTime: Long, title: String, tag: String): Pair<Long, Long> {
        val durationMillis = endTime - startTime
        val durationMinutes = durationMillis / 60000L
        val endCal = Calendar.getInstance().apply { timeInMillis = endTime }
        val endMinutes = endCal.get(Calendar.HOUR_OF_DAY) * 60 + endCal.get(Calendar.MINUTE)
        
        val titleLen = title.length
        val tagLen = tag.length
        val maxTextLen = maxOf(titleLen.toFloat(), tagLen.toFloat() * 0.8f)
        val estimatedWidthDp = 44 + (maxTextLen * 8)
        val visualMinutes = estimatedWidthDp / 1.5f
        val visualDurationMillis = (visualMinutes * 60 * 1000L).toLong()
        
        val alignTextEnd = durationMinutes < 150 && endMinutes > 22 * 60
        
        if (alignTextEnd) {
            val visualStart = endTime - maxOf(durationMillis, visualDurationMillis)
            return Pair(minOf(startTime, visualStart), endTime)
        } else {
            val visualEnd = startTime + maxOf(durationMillis, visualDurationMillis)
            return Pair(startTime, maxOf(endTime, visualEnd))
        }
    }

    val cal = Calendar.getInstance()
    cal.set(Calendar.HOUR_OF_DAY, 23)
    cal.set(Calendar.MINUTE, 0)
    val s1 = cal.timeInMillis
    cal.set(Calendar.HOUR_OF_DAY, 23)
    cal.set(Calendar.MINUTE, 59)
    val e1 = cal.timeInMillis
    
    val bounds = getVisualBounds(s1, e1, "Depart from station Vishakhapatnam", "Travel")
    val vStart = Calendar.getInstance().apply { timeInMillis = bounds.first }
    val vEnd = Calendar.getInstance().apply { timeInMillis = bounds.second }
    println("Actual: 23:00 to 23:59")
    println("Visual: ${vStart.get(Calendar.HOUR_OF_DAY)}:${vStart.get(Calendar.MINUTE)} to ${vEnd.get(Calendar.HOUR_OF_DAY)}:${vEnd.get(Calendar.MINUTE)}")
}
