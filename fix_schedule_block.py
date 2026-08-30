import re
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

sig_pattern = r"fun ScheduleBlock\(\s*schedule: DailyScheduleTask,\s*coloredCategoriesEnabled: Boolean,\s*use24HourFormat: Boolean,\s*isBleedLeft: Boolean,\s*isBleedRight: Boolean,\s*modifier: Modifier,\s*blockWidth: androidx.compose.ui.unit.Dp,\s*onClick: \(\) -> Unit,\s*onStatusChange: \(ScheduleStatus\) -> Unit\s*\)"
sig_replacement = """fun ScheduleBlock(
    schedule: DailyScheduleTask,
    coloredCategoriesEnabled: Boolean,
    use24HourFormat: Boolean,
    isBleedLeft: Boolean,
    isBleedRight: Boolean,
    isWarning: Boolean = false,
    elevation: androidx.compose.ui.unit.Dp = 0.dp,
    modifier: Modifier,
    blockWidth: androidx.compose.ui.unit.Dp,
    onClick: () -> Unit,
    onStatusChange: (ScheduleStatus) -> Unit
)"""

content = re.sub(sig_pattern, sig_replacement, content)

bg_opacity_pattern = r"val bgOpacity = if \(status == ScheduleStatus\.COMPLETED \|\| status == ScheduleStatus\.SKIPPED \|\| status == ScheduleStatus\.DROPPED\) 0\.08f else 0\.15f"
bg_opacity_replace = "val bgOpacity = if (isWarning) 0.5f else if (status == ScheduleStatus.COMPLETED || status == ScheduleStatus.SKIPPED || status == ScheduleStatus.DROPPED) 0.08f else 0.15f"
content = content.replace(bg_opacity_pattern, bg_opacity_replace)

block_bg_pattern = r"val blockBackgroundColor = if \(isUncategorized\) Color\.Transparent else tagColor\.copy\(alpha = bgOpacity\)"
block_bg_replace = "val blockBackgroundColor = if (isWarning) Color.Red.copy(alpha = bgOpacity) else if (isUncategorized) Color.Transparent else tagColor.copy(alpha = bgOpacity)"
content = content.replace(block_bg_pattern, block_bg_replace)

block_border_pattern = r"val blockBorderColor = if \(isUncategorized\) MaterialTheme\.colorScheme\.outlineVariant else tagColor\.copy\(alpha = borderOpacity\)"
block_border_replace = "val blockBorderColor = if (isWarning) Color.Red else if (isUncategorized) MaterialTheme.colorScheme.outlineVariant else tagColor.copy(alpha = borderOpacity)"
content = content.replace(block_border_pattern, block_border_replace)

box_mod_pattern = r"modifier = modifier"
box_mod_replace = "modifier = modifier.shadow(elevation, shape, clip = false)"
content = content.replace(box_mod_pattern, box_mod_replace, 1)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
