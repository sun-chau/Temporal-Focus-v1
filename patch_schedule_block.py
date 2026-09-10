import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# 1. Patch the drawing shape and shadow
shape_target = """    val blockBorderWidth = if (isUncategorized) 3.dp else 2.dp

    val shape = RoundedCornerShape(
        topStart = if (isBleedLeft) 0.dp else 8.dp,
        bottomStart = if (isBleedLeft) 0.dp else 8.dp,
        topEnd = if (isBleedRight) 0.dp else 8.dp,
        bottomEnd = if (isBleedRight) 0.dp else 8.dp
    )
    Box(
        modifier = modifier.shadow(elevation, shape, clip = false)
    ) {
        
        Box(
            modifier = Modifier
                .width(blockWidth)
                .fillMaxHeight()
                .clip(shape)
                .background(blockBackgroundColor)
                .drawBehind {
                    val stroke = androidx.compose.ui.graphics.drawscope.Stroke(blockBorderWidth.toPx())
                    val halfStroke = blockBorderWidth.toPx() / 2f
                    val cornerRadius = 8.dp.toPx()
                    
                    val path = androidx.compose.ui.graphics.Path().apply {
                        if (isBleedLeft) {
                            moveTo(0f, halfStroke)
                        } else {
                            moveTo(cornerRadius, halfStroke)
                        }
                        
                        // Top edge
                        if (isBleedRight) {
                            lineTo(size.width, halfStroke)
                        } else {
                            lineTo(size.width - cornerRadius, halfStroke)
                            arcTo(
                                rect = androidx.compose.ui.geometry.Rect(size.width - 2 * cornerRadius, halfStroke, size.width - halfStroke, 2 * cornerRadius - halfStroke),
                                startAngleDegrees = -90f,
                                sweepAngleDegrees = 90f,
                                forceMoveTo = false
                            )
                        }
                        
                        // Right edge
                        if (!isBleedRight) {
                            lineTo(size.width - halfStroke, size.height - cornerRadius)
                            arcTo(
                                rect = androidx.compose.ui.geometry.Rect(size.width - 2 * cornerRadius, size.height - 2 * cornerRadius + halfStroke, size.width - halfStroke, size.height - halfStroke),
                                startAngleDegrees = 0f,
                                sweepAngleDegrees = 90f,
                                forceMoveTo = false
                            )
                        } else {
                            moveTo(size.width, size.height - halfStroke)
                        }
                        
                        // Bottom edge
                        if (isBleedLeft) {
                            lineTo(0f, size.height - halfStroke)
                        } else {
                            lineTo(cornerRadius, size.height - halfStroke)
                            arcTo(
                                rect = androidx.compose.ui.geometry.Rect(halfStroke, size.height - 2 * cornerRadius + halfStroke, 2 * cornerRadius - halfStroke, size.height - halfStroke),
                                startAngleDegrees = 90f,
                                sweepAngleDegrees = 90f,
                                forceMoveTo = false
                            )
                        }
                        
                        // Left edge
                        if (!isBleedLeft) {
                            lineTo(halfStroke, cornerRadius)
                            arcTo(
                                rect = androidx.compose.ui.geometry.Rect(halfStroke, halfStroke, 2 * cornerRadius - halfStroke, 2 * cornerRadius - halfStroke),
                                startAngleDegrees = 180f,
                                sweepAngleDegrees = 90f,
                                forceMoveTo = false
                            )
                        } else {
                            moveTo(0f, halfStroke)
                        }
                    }
                    drawPath(path, blockBorderColor, style = stroke)
                }
                .clickable { onClick() }
        )"""
shape_replacement = """    val blockBorderWidth = if (isUncategorized) 3.dp else 2.dp
    val activeBorderColor = if (isWarning) Color.Red else MaterialTheme.colorScheme.primary
    val finalBorderColor = if (elevation > 0.dp) activeBorderColor else blockBorderColor
    val finalBgColor = if (elevation > 0.dp) blockBackgroundColor.copy(alpha = blockBackgroundColor.alpha + 0.15f) else blockBackgroundColor
    val finalBorderWidth = if (elevation > 0.dp) 2.dp else blockBorderWidth
    
    Box(
        modifier = modifier
    ) {
        
        Box(
            modifier = Modifier
                .width(blockWidth)
                .fillMaxHeight()
                .background(finalBgColor)
                .drawBehind {
                    val stroke = androidx.compose.ui.graphics.drawscope.Stroke(finalBorderWidth.toPx())
                    val halfStroke = finalBorderWidth.toPx() / 2f
                    
                    val path = androidx.compose.ui.graphics.Path().apply {
                        if (isBleedLeft) {
                            moveTo(0f, halfStroke)
                        } else {
                            moveTo(halfStroke, halfStroke)
                        }
                        
                        // Top edge
                        if (isBleedRight) {
                            lineTo(size.width, halfStroke)
                        } else {
                            lineTo(size.width - halfStroke, halfStroke)
                        }
                        
                        // Right edge
                        if (!isBleedRight) {
                            lineTo(size.width - halfStroke, size.height - halfStroke)
                        } else {
                            moveTo(size.width, size.height - halfStroke)
                        }
                        
                        // Bottom edge
                        if (isBleedLeft) {
                            lineTo(0f, size.height - halfStroke)
                        } else {
                            lineTo(halfStroke, size.height - halfStroke)
                        }
                        
                        // Left edge
                        if (!isBleedLeft) {
                            lineTo(halfStroke, halfStroke)
                        } else {
                            moveTo(0f, halfStroke)
                        }
                    }
                    drawPath(path, finalBorderColor, style = stroke)
                }
                .clickable { onClick() }
        )"""

content = content.replace(shape_target, shape_replacement)

# 2. Patch Floating Label for Dragging and Text styling
floating_target = """        // Floating Label for Dragging
        if (elevation > 0.dp) {
            Box(
                modifier = Modifier
                    .offset(y = (-24).dp)
                    .align(Alignment.TopCenter)
                    .background(if (isWarning) Color.Red else MaterialTheme.colorScheme.primary, RoundedCornerShape(4.dp))
                    .padding(horizontal = 6.dp, vertical = 2.dp)
            ) {
                Text(
                    text = "$startStr - $endStr",
                    color = MaterialTheme.colorScheme.onPrimary,
                    style = MaterialTheme.typography.labelSmall,
                    fontWeight = FontWeight.Bold
                )
            }
        }
        
        // Content layer (allowed to bleed horizontally)
        Row(
            modifier = Modifier
                .width(blockWidth)
                .wrapContentWidth(unbounded = true, align = if (alignTextEnd) Alignment.End else Alignment.Start)
                .fillMaxHeight()
                .padding(horizontal = 8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(
                modifier = Modifier
                    .padding(end = 8.dp)
                    .clickable { onClick() },
                verticalArrangement = Arrangement.Center
            ) {
                Text(
                    text = schedule.title, 
                    fontWeight = FontWeight.Bold, 
                    fontSize = 15.sp, 
                    color = textColor,
                    maxLines = 1,
                    softWrap = false
                )
                if (schedule.label.isNotBlank()) {
                    Text(
                        text = getLabelName(schedule.label), 
                        fontSize = 12.sp, 
                        color = subTextColor,
                        maxLines = 1,
                        softWrap = false
                    )
                }
                Spacer(modifier = Modifier.height(2.dp))
                Text(
                    text = "$startStr - $endStr", 
                    fontSize = 11.sp, 
                    color = subTextColor,
                    maxLines = 1,
                    softWrap = false
                )
            }
            
            // Status Icon appended to the right of the text
            Box(
                modifier = Modifier
                    .size(28.dp)
                    .clip(CircleShape)
                    .background(if (isUncategorized) Color.Transparent else if (status == ScheduleStatus.COMPLETED) Color.Gray.copy(alpha = 0.2f) else MaterialTheme.colorScheme.surfaceVariant)
                    .then(if (isUncategorized) Modifier.border(2.dp, iconBorderColor, CircleShape) else Modifier)
                    .clickable { 
                        if (enableRadioMenu) {
                            showStatusMenu = true 
                        } else {
                            val nextStatus = if (status == ScheduleStatus.NOT_DONE) ScheduleStatus.COMPLETED else ScheduleStatus.NOT_DONE
                            onStatusChange(nextStatus)
                        }
                    },
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = when (status) {
                        ScheduleStatus.COMPLETED -> Icons.Default.CheckCircle
                        ScheduleStatus.SKIPPED -> Icons.Default.FastForward
                        ScheduleStatus.DROPPED -> Icons.Default.Cancel
                        else -> Icons.Outlined.RadioButtonUnchecked
                    },
                    contentDescription = "Status",
                    tint = textColor,
                    modifier = Modifier.size(18.dp)
                )"""

floating_replacement = """        // Floating Label for Dragging
        if (elevation > 0.dp) {
            Box(
                modifier = Modifier
                    .offset(y = (-24).dp)
                    .align(Alignment.TopCenter)
                    .background(if (isWarning) Color.Red else MaterialTheme.colorScheme.primary, RectangleShape)
                    .padding(horizontal = 6.dp, vertical = 2.dp)
            ) {
                Text(
                    text = "[ $startStr - $endStr ]",
                    fontFamily = FontFamily.Monospace,
                    color = MaterialTheme.colorScheme.onPrimary,
                    style = MaterialTheme.typography.labelSmall,
                    fontWeight = FontWeight.Bold
                )
            }
        }
        
        // Content layer (allowed to bleed horizontally)
        Row(
            modifier = Modifier
                .width(blockWidth)
                .wrapContentWidth(unbounded = true, align = if (alignTextEnd) Alignment.End else Alignment.Start)
                .fillMaxHeight()
                .padding(horizontal = 8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(
                modifier = Modifier
                    .padding(end = 8.dp)
                    .clickable { onClick() },
                verticalArrangement = Arrangement.Center
            ) {
                Text(
                    text = schedule.title.uppercase(java.util.Locale.getDefault()), 
                    fontFamily = FontFamily.Monospace,
                    fontWeight = FontWeight.Bold, 
                    fontSize = 15.sp, 
                    color = textColor,
                    maxLines = 1,
                    softWrap = false
                )
                if (schedule.label.isNotBlank()) {
                    Text(
                        text = getLabelName(schedule.label).uppercase(java.util.Locale.getDefault()), 
                        fontFamily = FontFamily.Monospace,
                        fontSize = 12.sp, 
                        color = subTextColor,
                        maxLines = 1,
                        softWrap = false
                    )
                }
                Spacer(modifier = Modifier.height(2.dp))
                Text(
                    text = "[ $startStr - $endStr ]", 
                    fontFamily = FontFamily.Monospace,
                    fontSize = 11.sp, 
                    color = subTextColor,
                    maxLines = 1,
                    softWrap = false
                )
            }
            
            // Status Text Checkbox
            Box(
                modifier = Modifier
                    .background(Color.Transparent)
                    .border(1.dp, if (iconBorderColor == Color.Transparent) textColor.copy(alpha=0.5f) else iconBorderColor, RectangleShape)
                    .clickable { 
                        if (enableRadioMenu) {
                            showStatusMenu = true 
                        } else {
                            val nextStatus = if (status == ScheduleStatus.NOT_DONE) ScheduleStatus.COMPLETED else ScheduleStatus.NOT_DONE
                            onStatusChange(nextStatus)
                        }
                    }
                    .padding(horizontal = 4.dp, vertical = 2.dp),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = when (status) {
                        ScheduleStatus.COMPLETED -> "[X]"
                        ScheduleStatus.SKIPPED -> "[-]"
                        ScheduleStatus.DROPPED -> "[/]"
                        else -> "[ ]"
                    },
                    fontFamily = FontFamily.Monospace,
                    color = textColor,
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Bold
                )"""

content = content.replace(floating_target, floating_replacement)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
print("ScheduleBlock Patched")
