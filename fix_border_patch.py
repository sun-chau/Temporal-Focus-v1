with open("app/src/main/java/com/example/ui/screens/UserAccountScreen.kt", "r") as f:
    content = f.read()

# Add imports for border
imports = """
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.border
import androidx.compose.foundation.BorderStroke
"""
if "import androidx.compose.foundation.isSystemInDarkTheme" not in content:
    content = content.replace("import com.example.viewmodel.MainViewModel", imports + "import com.example.viewmodel.MainViewModel")

# Add dark theme detection at top
if "val isDarkTheme = isSystemInDarkTheme()" not in content:
    content = content.replace("val allAvailableColors", "val isDarkTheme = isSystemInDarkTheme()\n    val outlineColor = if (isDarkTheme) Color.White.copy(alpha = 0.2f) else Color.Black.copy(alpha = 0.2f)\n    val allAvailableColors")

# Add border to tag Box
tag_box_old = """.clip(CircleShape)
                                    .background(try { Color(android.graphics.Color.parseColor(tagColor)) } catch(e:Exception){MaterialTheme.colorScheme.onSurfaceVariant})
                                    .pointerInput(Unit)"""
tag_box_new = """.clip(CircleShape)
                                    .background(try { Color(android.graphics.Color.parseColor(tagColor)) } catch(e:Exception){MaterialTheme.colorScheme.onSurfaceVariant})
                                    .border(1.dp, outlineColor, CircleShape)
                                    .pointerInput(Unit)"""
content = content.replace(tag_box_old, tag_box_new)

# Add border to category Box
cat_box_old = """.clip(CircleShape)
                                    .background(try { Color(android.graphics.Color.parseColor(categoryColor)) } catch(e:Exception){MaterialTheme.colorScheme.onSurfaceVariant})
                                    .pointerInput(Unit)"""
cat_box_new = """.clip(CircleShape)
                                    .background(try { Color(android.graphics.Color.parseColor(categoryColor)) } catch(e:Exception){MaterialTheme.colorScheme.onSurfaceVariant})
                                    .border(1.dp, outlineColor, CircleShape)
                                    .pointerInput(Unit)"""
content = content.replace(cat_box_old, cat_box_new)

with open("app/src/main/java/com/example/ui/screens/UserAccountScreen.kt", "w") as f:
    f.write(content)
