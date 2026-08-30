with open("app/src/main/java/com/example/ui/screens/UserAccountScreen.kt", "r") as f:
    content = f.read()

old_cat = """.clip(androidx.compose.foundation.shape.CircleShape)
                                    .background(try { Color(android.graphics.Color.parseColor(categoryColor)) } catch(e:Exception){MaterialTheme.colorScheme.onSurfaceVariant})
                                    .clickable { categoryColor = allAvailableColors.randomOrNull() ?: "#9E9E9E" }"""

new_cat = """.clip(androidx.compose.foundation.shape.CircleShape)
                                    .background(try { Color(android.graphics.Color.parseColor(categoryColor)) } catch(e:Exception){MaterialTheme.colorScheme.onSurfaceVariant})
                                    .border(1.dp, outlineColor, androidx.compose.foundation.shape.CircleShape)
                                    .pointerInput(Unit) {
                                        detectTapGestures(
                                            onTap = { _ -> categoryColor = allAvailableColors.randomOrNull() ?: "#9E9E9E" },
                                            onLongPress = { showCategoryColorPalette = true }
                                        )
                                    }"""

content = content.replace(old_cat, new_cat)

with open("app/src/main/java/com/example/ui/screens/UserAccountScreen.kt", "w") as f:
    f.write(content)
