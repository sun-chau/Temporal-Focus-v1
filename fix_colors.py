import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Replace variables
old_vars = """    val bgOpacity = if (status == ScheduleStatus.COMPLETED || status == ScheduleStatus.SKIPPED || status == ScheduleStatus.DROPPED) 0.08f else 0.15f
    val borderOpacity = if (status == ScheduleStatus.COMPLETED || status == ScheduleStatus.SKIPPED || status == ScheduleStatus.DROPPED) 0.4f else 1.0f

    val blockBackgroundColor = if (isUncategorized) Color.Transparent else tagColor.copy(alpha = bgOpacity)
    val blockBorderColor = if (isUncategorized) MaterialTheme.colorScheme.onSurface else tagColor.copy(alpha = borderOpacity)
    val blockBorderWidth = if (isUncategorized) 3.dp else 2.dp"""

new_vars = """    val onSurfaceColor = MaterialTheme.colorScheme.onSurface
    
    val targetBorderColor = if (status == ScheduleStatus.COMPLETED) {
        Color.Gray
    } else if (isUncategorized) {
        onSurfaceColor
    } else {
        val borderOpacity = if (status == ScheduleStatus.SKIPPED || status == ScheduleStatus.DROPPED) 0.4f else 1.0f
        tagColor.copy(alpha = borderOpacity)
    }

    val targetBackgroundColor = if (status == ScheduleStatus.COMPLETED) {
        Color.Gray.copy(alpha = 0.20f)
    } else if (isUncategorized) {
        onSurfaceColor.copy(alpha = 0.03f)
    } else {
        val bgOpacity = if (status == ScheduleStatus.SKIPPED || status == ScheduleStatus.DROPPED) 0.08f else 0.20f
        tagColor.copy(alpha = bgOpacity)
    }

    val targetTextColor = if (status == ScheduleStatus.COMPLETED) {
        Color.Gray
    } else {
        onSurfaceColor
    }
    
    val targetSubTextColor = if (status == ScheduleStatus.COMPLETED) {
        Color.Gray
    } else {
        MaterialTheme.colorScheme.onSurfaceVariant
    }

    val blockBorderColor by androidx.compose.animation.animateColorAsState(
        targetValue = targetBorderColor,
        animationSpec = androidx.compose.animation.core.tween(durationMillis = 200),
        label = "blockBorderColor"
    )
    val blockBackgroundColor by androidx.compose.animation.animateColorAsState(
        targetValue = targetBackgroundColor,
        animationSpec = androidx.compose.animation.core.tween(durationMillis = 200),
        label = "blockBackgroundColor"
    )
    val textColor by androidx.compose.animation.animateColorAsState(
        targetValue = targetTextColor,
        animationSpec = androidx.compose.animation.core.tween(durationMillis = 200),
        label = "textColor"
    )
    val subTextColor by androidx.compose.animation.animateColorAsState(
        targetValue = targetSubTextColor,
        animationSpec = androidx.compose.animation.core.tween(durationMillis = 200),
        label = "subTextColor"
    )
    
    val targetIconBorderColor = if (status == ScheduleStatus.COMPLETED && isUncategorized) {
        Color.Gray
    } else if (isUncategorized) {
        onSurfaceColor
    } else {
        Color.Transparent
    }
    
    val iconBorderColor by androidx.compose.animation.animateColorAsState(
        targetValue = targetIconBorderColor,
        animationSpec = androidx.compose.animation.core.tween(durationMillis = 200),
        label = "iconBorderColor"
    )

    val blockBorderWidth = if (isUncategorized) 3.dp else 2.dp"""

content = content.replace(old_vars, new_vars)

old_title = """                Text(
                    text = schedule.title, 
                    fontWeight = FontWeight.Bold, 
                    fontSize = 15.sp, 
                    color = MaterialTheme.colorScheme.onSurface,
                    maxLines = 1,
                    softWrap = false
                )"""
new_title = """                Text(
                    text = schedule.title, 
                    fontWeight = FontWeight.Bold, 
                    fontSize = 15.sp, 
                    color = textColor,
                    maxLines = 1,
                    softWrap = false
                )"""
content = content.replace(old_title, new_title)

old_tag = """                    Text(
                        text = getTagName(schedule.tag), 
                        fontSize = 12.sp, 
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 1,
                        softWrap = false
                    )"""
new_tag = """                    Text(
                        text = getTagName(schedule.tag), 
                        fontSize = 12.sp, 
                        color = subTextColor,
                        maxLines = 1,
                        softWrap = false
                    )"""
content = content.replace(old_tag, new_tag)

old_time = """                Text(
                    text = "$startStr - $endStr", 
                    fontSize = 11.sp, 
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    softWrap = false
                )"""
new_time = """                Text(
                    text = "$startStr - $endStr", 
                    fontSize = 11.sp, 
                    color = subTextColor,
                    maxLines = 1,
                    softWrap = false
                )"""
content = content.replace(old_time, new_time)

old_icon_bg = """                    .background(if (isUncategorized) Color.Transparent else MaterialTheme.colorScheme.surfaceVariant)
                    .then(if (isUncategorized) Modifier.border(2.dp, MaterialTheme.colorScheme.onSurface, CircleShape) else Modifier)"""

new_icon_bg = """                    .background(if (isUncategorized) Color.Transparent else if (status == ScheduleStatus.COMPLETED) Color.Gray.copy(alpha = 0.2f) else MaterialTheme.colorScheme.surfaceVariant)
                    .then(if (isUncategorized) Modifier.border(2.dp, iconBorderColor, CircleShape) else Modifier)"""
content = content.replace(old_icon_bg, new_icon_bg)

old_icon_tint = """                    tint = MaterialTheme.colorScheme.onSurface,"""
new_icon_tint = """                    tint = textColor,"""
content = content.replace(old_icon_tint, new_icon_tint)


with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)

