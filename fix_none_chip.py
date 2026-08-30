import sys

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

old_lazy_row = """            LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                items(tags) { tag ->
                    val isSelected = selectedTag == tag
                    val color = getTagColor(tag, true)
                    
                    Box(
                        modifier = Modifier
                            .height(36.dp)
                            .clip(RoundedCornerShape(16.dp))
                            .background(if (isSelected) color else color.copy(alpha = 0.2f))
                            .clickable { selectedTag = if (selectedTag == tag) "" else tag }
                            .padding(horizontal = 12.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = getTagName(tag),
                            color = if (isSelected) MaterialTheme.colorScheme.onSurface else color,
                            fontSize = 16.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }
            }"""

new_lazy_row = """            LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                item {
                    val isNoneSelected = selectedTag.isBlank()
                    Box(
                        modifier = Modifier
                            .height(36.dp)
                            .clip(RoundedCornerShape(16.dp))
                            .background(if (isNoneSelected) MaterialTheme.colorScheme.surfaceVariant else Color.Transparent)
                            .border(1.dp, MaterialTheme.colorScheme.outlineVariant, RoundedCornerShape(16.dp))
                            .clickable { selectedTag = "" }
                            .padding(horizontal = 12.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.NotInterested, contentDescription = "None", modifier = Modifier.size(16.dp).padding(end = 4.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant)
                            Text(
                                text = "None",
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                fontSize = 16.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }
                }
                items(tags) { tag ->
                    val isSelected = selectedTag == tag
                    val color = getTagColor(tag, true)
                    
                    Box(
                        modifier = Modifier
                            .height(36.dp)
                            .clip(RoundedCornerShape(16.dp))
                            .background(if (isSelected) color else color.copy(alpha = 0.2f))
                            .clickable { selectedTag = if (selectedTag == tag) "" else tag }
                            .padding(horizontal = 12.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = getTagName(tag),
                            color = if (isSelected) MaterialTheme.colorScheme.onSurface else color,
                            fontSize = 16.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }
            }"""

if old_lazy_row in content:
    content = content.replace(old_lazy_row, new_lazy_row)
else:
    print("Failed to replace lazy row")
    sys.exit(1)

# Check if NotInterested is imported
if "import androidx.compose.material.icons.filled.NotInterested" not in content:
    content = content.replace("import androidx.compose.material.icons.filled.Add", "import androidx.compose.material.icons.filled.Add\nimport androidx.compose.material.icons.filled.NotInterested")

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
