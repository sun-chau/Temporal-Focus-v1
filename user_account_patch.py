import re

with open("app/src/main/java/com/example/ui/screens/UserAccountScreen.kt", "r") as f:
    content = f.read()

# Add imports
imports = """
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.ui.input.pointer.pointerInput
import com.example.ui.components.ColorPaletteBottomSheet
import com.example.ui.components.STANDARD_PALETTE
"""
if "import com.example.ui.components.ColorPaletteBottomSheet" not in content:
    content = content.replace("import com.example.viewmodel.MainViewModel", imports + "import com.example.viewmodel.MainViewModel")


# Replace tagColor and categoryColor initialization
init_replace = """
    val allAvailableColors = remember(uiState.customColors) { STANDARD_PALETTE + uiState.customColors.toList() }
    var newTag by remember { mutableStateOf("") }
    var tagColor by remember { mutableStateOf(allAvailableColors.randomOrNull() ?: "#9E9E9E") }
    var newCategory by remember { mutableStateOf("") }
    var categoryColor by remember { mutableStateOf(allAvailableColors.randomOrNull() ?: "#9E9E9E") }
    
    var showTagColorPalette by remember { mutableStateOf(false) }
    var showCategoryColorPalette by remember { mutableStateOf(false) }
"""
content = re.sub(r'var newTag by remember \{ mutableStateOf\(""\) \}.*?var categoryColor by remember \{ mutableStateOf\(String\.format[^\}]+\) \}', init_replace, content, flags=re.DOTALL)


# Replace tag color box
tag_box_old = """.size(24.dp)
                                    .clip(CircleShape)
                                    .background(try { Color(android.graphics.Color.parseColor(tagColor)) } catch(e:Exception){MaterialTheme.colorScheme.onSurfaceVariant})
                                    .clickable { tagColor = String.format("#%02X%02X%02X", (0..255).random(), (0..255).random(), (0..255).random()) }"""

tag_box_new = """.size(24.dp)
                                    .clip(CircleShape)
                                    .background(try { Color(android.graphics.Color.parseColor(tagColor)) } catch(e:Exception){MaterialTheme.colorScheme.onSurfaceVariant})
                                    .pointerInput(Unit) {
                                        detectTapGestures(
                                            onClick = { tagColor = allAvailableColors.randomOrNull() ?: "#9E9E9E" },
                                            onLongPress = { showTagColorPalette = true }
                                        )
                                    }"""
content = content.replace(tag_box_old, tag_box_new)


# Replace tag reset
tag_reset_old = """tagColor = String.format("#%02X%02X%02X", (0..255).random(), (0..255).random(), (0..255).random())"""
tag_reset_new = """tagColor = allAvailableColors.randomOrNull() ?: "#9E9E9E\""""
content = content.replace(tag_reset_old, tag_reset_new)


# Replace category color box
cat_box_old = """.size(24.dp)
                                    .clip(CircleShape)
                                    .background(try { Color(android.graphics.Color.parseColor(categoryColor)) } catch(e:Exception){MaterialTheme.colorScheme.onSurfaceVariant})
                                    .clickable { categoryColor = String.format("#%02X%02X%02X", (0..255).random(), (0..255).random(), (0..255).random()) }"""

cat_box_new = """.size(24.dp)
                                    .clip(CircleShape)
                                    .background(try { Color(android.graphics.Color.parseColor(categoryColor)) } catch(e:Exception){MaterialTheme.colorScheme.onSurfaceVariant})
                                    .pointerInput(Unit) {
                                        detectTapGestures(
                                            onClick = { categoryColor = allAvailableColors.randomOrNull() ?: "#9E9E9E" },
                                            onLongPress = { showCategoryColorPalette = true }
                                        )
                                    }"""
content = content.replace(cat_box_old, cat_box_new)


# Replace category reset
cat_reset_old = """categoryColor = String.format("#%02X%02X%02X", (0..255).random(), (0..255).random(), (0..255).random())"""
cat_reset_new = """categoryColor = allAvailableColors.randomOrNull() ?: "#9E9E9E\""""
content = content.replace(cat_reset_old, cat_reset_new)


# Insert ColorPaletteBottomSheets at the end of the top-level Column/Scaffold (before the last closing brace)
sheets_code = """
        ColorPaletteBottomSheet(
            isVisible = showTagColorPalette,
            onDismiss = { showTagColorPalette = false },
            selectedColorHex = tagColor,
            customColors = uiState.customColors,
            onColorSelected = { tagColor = it },
            onReset = { tagColor = allAvailableColors.randomOrNull() ?: "#9E9E9E" },
            onAddCustomColor = { viewModel.addCustomColor(it); tagColor = it }
        )

        ColorPaletteBottomSheet(
            isVisible = showCategoryColorPalette,
            onDismiss = { showCategoryColorPalette = false },
            selectedColorHex = categoryColor,
            customColors = uiState.customColors,
            onColorSelected = { categoryColor = it },
            onReset = { categoryColor = allAvailableColors.randomOrNull() ?: "#9E9E9E" },
            onAddCustomColor = { viewModel.addCustomColor(it); categoryColor = it }
        )
"""
# Find the last brace and insert before it
last_brace = content.rfind("}")
content = content[:last_brace] + sheets_code + "\n}\n"

with open("app/src/main/java/com/example/ui/screens/UserAccountScreen.kt", "w") as f:
    f.write(content)
