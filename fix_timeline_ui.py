import sys

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

old_block_start = """    val baseTagColor = getTagColor(schedule.tag, coloredCategoriesEnabled)
    val tagColor = if (baseTagColor != Color.Transparent) baseTagColor else androidx.compose.material3.MaterialTheme.colorScheme.primary
    var showStatusMenu by remember { mutableStateOf(false) }
    
    val startCal = Calendar.getInstance().apply { timeInMillis = schedule.startTime }
    val endCal = Calendar.getInstance().apply { timeInMillis = schedule.endTime }
    val startStr = String.format("%02d:%02d", startCal.get(Calendar.HOUR_OF_DAY), startCal.get(Calendar.MINUTE))
    val endStr = String.format("%02d:%02d", endCal.get(Calendar.HOUR_OF_DAY), endCal.get(Calendar.MINUTE))
    
    val status = try { ScheduleStatus.valueOf(schedule.status) } catch (e: Exception) { ScheduleStatus.NOT_DONE }
    
    val bgOpacity = if (status == ScheduleStatus.COMPLETED || status == ScheduleStatus.SKIPPED || status == ScheduleStatus.DROPPED) 0.08f else 0.15f
    val borderOpacity = if (status == ScheduleStatus.COMPLETED || status == ScheduleStatus.SKIPPED || status == ScheduleStatus.DROPPED) 0.4f else 1.0f

    Box(
        modifier = modifier
    ) {
        // Colored background layer (strictly constrained to blockWidth)
        Box(
            modifier = Modifier
                .width(blockWidth)
                .fillMaxHeight()
                .clip(RoundedCornerShape(8.dp))
                .background(tagColor.copy(alpha = bgOpacity))
                .border(2.dp, tagColor.copy(alpha = borderOpacity), RoundedCornerShape(8.dp))
                .clickable { onClick() }
        )"""

new_block_start = """    val isUncategorized = schedule.tag.isBlank()
    val baseTagColor = getTagColor(schedule.tag, coloredCategoriesEnabled)
    val tagColor = if (baseTagColor != Color.Transparent) baseTagColor else androidx.compose.material3.MaterialTheme.colorScheme.primary
    var showStatusMenu by remember { mutableStateOf(false) }
    
    val startCal = Calendar.getInstance().apply { timeInMillis = schedule.startTime }
    val endCal = Calendar.getInstance().apply { timeInMillis = schedule.endTime }
    val startStr = String.format("%02d:%02d", startCal.get(Calendar.HOUR_OF_DAY), startCal.get(Calendar.MINUTE))
    val endStr = String.format("%02d:%02d", endCal.get(Calendar.HOUR_OF_DAY), endCal.get(Calendar.MINUTE))
    
    val status = try { ScheduleStatus.valueOf(schedule.status) } catch (e: Exception) { ScheduleStatus.NOT_DONE }
    
    val bgOpacity = if (status == ScheduleStatus.COMPLETED || status == ScheduleStatus.SKIPPED || status == ScheduleStatus.DROPPED) 0.08f else 0.15f
    val borderOpacity = if (status == ScheduleStatus.COMPLETED || status == ScheduleStatus.SKIPPED || status == ScheduleStatus.DROPPED) 0.4f else 1.0f

    val blockBackgroundColor = if (isUncategorized) Color.Transparent else tagColor.copy(alpha = bgOpacity)
    val blockBorderColor = if (isUncategorized) MaterialTheme.colorScheme.outlineVariant else tagColor.copy(alpha = borderOpacity)
    val blockBorderWidth = if (isUncategorized) 1.dp else 2.dp

    Box(
        modifier = modifier
    ) {
        // Colored background layer (strictly constrained to blockWidth)
        Box(
            modifier = Modifier
                .width(blockWidth)
                .fillMaxHeight()
                .clip(RoundedCornerShape(8.dp))
                .background(blockBackgroundColor)
                .border(blockBorderWidth, blockBorderColor, RoundedCornerShape(8.dp))
                .clickable { onClick() }
        )"""

if old_block_start in content:
    content = content.replace(old_block_start, new_block_start)
else:
    print("Failed to replace block_start")
    sys.exit(1)

old_status_icon = """            // Status Icon appended to the right of the text
            Box(
                modifier = Modifier
                    .size(28.dp)
                    .clip(CircleShape)
                    .background(MaterialTheme.colorScheme.surfaceVariant)
                    .clickable { showStatusMenu = true },
                contentAlignment = Alignment.Center
            ) {"""

new_status_icon = """            // Status Icon appended to the right of the text
            Box(
                modifier = Modifier
                    .size(28.dp)
                    .clip(CircleShape)
                    .background(if (isUncategorized) Color.Transparent else MaterialTheme.colorScheme.surfaceVariant)
                    .then(if (isUncategorized) Modifier.border(1.dp, MaterialTheme.colorScheme.outlineVariant, CircleShape) else Modifier)
                    .clickable { showStatusMenu = true },
                contentAlignment = Alignment.Center
            ) {"""

if old_status_icon in content:
    content = content.replace(old_status_icon, new_status_icon)
else:
    print("Failed to replace status_icon")
    sys.exit(1)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)

