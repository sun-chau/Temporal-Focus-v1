import re

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "r") as f:
    content = f.read()

search_str = r'''                                    displayTasks\.forEachIndexed \{ index, _ ->
                                        val isSelected = index == firstVisibleIndex
                                        val height = if \(isSelected\) 16\.dp else 6\.dp
                                        val color = if \(isSelected\) MaterialTheme\.colorScheme\.primary else Color\.DarkGray
                                        Box\(
                                            modifier = Modifier
                                                \.padding\(vertical = 2\.dp\)
                                                \.width\(6\.dp\)
                                                \.height\(height\)
                                                \.clip\(RoundedCornerShape\(3\.dp\)\)
                                                \.background\(color\)
                                        \)
                                    \}'''

replace_str = '''                                    displayTasks.forEachIndexed { index, _ ->
                                        val isSelected = index == firstVisibleIndex
                                        val animatedHeight by androidx.compose.animation.core.animateDpAsState(targetValue = if (isSelected) 24.dp else 8.dp, label = "height")
                                        val animatedColor by androidx.compose.animation.animateColorAsState(targetValue = if (isSelected) MaterialTheme.colorScheme.primary else Color.DarkGray, label = "color")
                                        Box(
                                            modifier = Modifier
                                                .padding(vertical = 4.dp)
                                                .width(6.dp)
                                                .height(animatedHeight)
                                                .clip(RoundedCornerShape(3.dp))
                                                .background(animatedColor)
                                        )
                                    }'''

content = re.sub(search_str, replace_str, content)

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "w") as f:
    f.write(content)
