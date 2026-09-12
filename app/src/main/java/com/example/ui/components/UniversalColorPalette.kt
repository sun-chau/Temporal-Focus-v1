package com.example.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.ui.graphics.RectangleShape
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Check
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.graphics.PathEffect
import androidx.compose.foundation.border

val STANDARD_PALETTE = listOf(
    "#F44336", "#E91E63", "#9C27B0", "#673AB7", "#3F51B5",
    "#2196F3", "#03A9F4", "#00BCD4", "#009688", "#4CAF50",
    "#8BC34A", "#CDDC39", "#FFEB3B", "#FFC107", "#FF9800",
    "#FF5722", "#795548", "#9E9E9E", "#607D8B"
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ColorPaletteBottomSheet(
    isVisible: Boolean,
    onDismiss: () -> Unit,
    selectedColorHex: String,
    customColors: Set<String>,
    onColorSelected: (String) -> Unit,
    onReset: () -> Unit,
    onAddCustomColor: (String) -> Unit
) {
    if (!isVisible) return

    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    var showCustomColorDialog by remember { mutableStateOf(false) }

    val allColors = remember(customColors) {
        STANDARD_PALETTE + customColors.toList()
    }

    ModalBottomSheet(
        onDismissRequest = onDismiss,
        sheetState = sheetState,
        shape = RectangleShape,
        dragHandle = { BottomSheetDefaults.DragHandle() }
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp)
                .padding(bottom = 32.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "SELECT COLOR",
                    style = MaterialTheme.typography.titleLarge,
                    fontFamily = FontFamily.Monospace,
                    fontWeight = FontWeight.Bold
                )
                TextButton(onClick = { onReset(); onDismiss() }) {
                    Text("[ RESET ]", fontFamily = FontFamily.Monospace)
                }
            }
            Spacer(modifier = Modifier.height(16.dp))

            LazyVerticalGrid(
                columns = GridCells.Adaptive(minSize = 56.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                items(allColors) { hex ->
                    ColorSwatch(
                        hexString = hex,
                        isSelected = selectedColorHex.equals(hex, ignoreCase = true),
                        onClick = {
                            onColorSelected(hex)
                            onDismiss()
                        }
                    )
                }

                item {
                    AddCustomColorButton {
                        showCustomColorDialog = true
                    }
                }
            }
        }
    }

    if (showCustomColorDialog) {
        CustomColorDialog(
            onDismiss = { showCustomColorDialog = false },
            onSave = { hex ->
                onAddCustomColor(hex)
                showCustomColorDialog = false
            }
        )
    }
}

@Composable
fun ColorSwatch(
    hexString: String,
    isSelected: Boolean,
    onClick: () -> Unit
) {
    val color = try {
        Color(android.graphics.Color.parseColor(hexString))
    } catch (e: Exception) {
        Color.Transparent
    }

    // Dynamic contrast border: White in dark mode, Black in light mode
    val isDarkTheme = isSystemInDarkTheme()
    val borderColor = if (isDarkTheme) Color.White.copy(alpha = 0.2f) else Color.Black.copy(alpha = 0.2f)

    Box(
        modifier = Modifier
            .size(56.dp)
            .clip(RectangleShape)
            .background(color)
            .border(BorderStroke(1.dp, borderColor), RectangleShape)
            .clickable(onClick = onClick),
        contentAlignment = Alignment.Center
    ) {
        if (isSelected) {
            val checkColor = if (color.luminance() > 0.5f) Color.Black else Color.White
            Icon(
                imageVector = Icons.Default.Check,
                contentDescription = "Selected",
                tint = checkColor,
                modifier = Modifier.size(24.dp)
            )
        }
    }
}

@Composable
fun AddCustomColorButton(onClick: () -> Unit) {
    val borderColor = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)
    Box(
        modifier = Modifier
            .size(56.dp)
            .clip(RectangleShape)
            .clickable(onClick = onClick),
        contentAlignment = Alignment.Center
    ) {
        // Dashed border
        androidx.compose.foundation.Canvas(modifier = Modifier.fillMaxSize()) {
            drawRect(
                color = borderColor,
                style = androidx.compose.ui.graphics.drawscope.Stroke(
                    width = 1.dp.toPx(),
                    pathEffect = PathEffect.dashPathEffect(floatArrayOf(10f, 10f), 0f)
                )
            )
        }
        Icon(
            imageVector = Icons.Default.Add,
            contentDescription = "Add Custom Color",
            tint = MaterialTheme.colorScheme.onSurface,
            modifier = Modifier.size(24.dp)
        )
    }
}

@Composable
fun CustomColorDialog(
    onDismiss: () -> Unit,
    onSave: (String) -> Unit
) {
    var hexInput by remember { mutableStateOf("#") }
    var previewColor by remember { mutableStateOf(Color.Transparent) }
    var r by remember { mutableFloatStateOf(255f) }
    var g by remember { mutableFloatStateOf(255f) }
    var b by remember { mutableFloatStateOf(255f) }
    var isUpdatingFromHex by remember { mutableStateOf(false) }

    fun updateHexFromRGB() {
        if (isUpdatingFromHex) return
        val hex = String.format("#%02X%02X%02X", r.toInt(), g.toInt(), b.toInt())
        hexInput = hex
        previewColor = Color(r.toInt(), g.toInt(), b.toInt())
    }
    
    fun updateRGBFromHex(hex: String) {
        if (hex.length == 7 && hex.startsWith("#")) {
            try {
                val parsed = android.graphics.Color.parseColor(hex)
                isUpdatingFromHex = true
                r = android.graphics.Color.red(parsed).toFloat()
                g = android.graphics.Color.green(parsed).toFloat()
                b = android.graphics.Color.blue(parsed).toFloat()
                previewColor = Color(parsed)
                isUpdatingFromHex = false
            } catch (e: Exception) {
                // Ignore invalid
            }
        }
    }

    LaunchedEffect(r, g, b) {
        updateHexFromRGB()
    }

    AlertDialog(
        onDismissRequest = onDismiss,
        shape = RectangleShape,
        title = { Text("CUSTOM COLOR", fontFamily = FontFamily.Monospace) },
        text = {
            Column(modifier = Modifier.fillMaxWidth()) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.Center
                ) {
                    val isDarkTheme = isSystemInDarkTheme()
                    val borderColor = if (isDarkTheme) Color.White.copy(alpha = 0.2f) else Color.Black.copy(alpha = 0.2f)
                    Box(
                        modifier = Modifier
                            .size(80.dp)
                            .clip(RectangleShape)
                            .background(previewColor)
                            .border(1.dp, borderColor, RectangleShape)
                    )
                }
                Spacer(modifier = Modifier.height(16.dp))
                OutlinedTextField(
                    value = hexInput,
                    onValueChange = {
                        hexInput = it
                        updateRGBFromHex(it)
                    },
                    label = { Text("Hex Color Code", fontFamily = FontFamily.Monospace) },
                    textStyle = MaterialTheme.typography.bodyLarge.copy(fontFamily = FontFamily.Monospace),
                    shape = RectangleShape,
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
                Spacer(modifier = Modifier.height(16.dp))
                Text("Red: ${r.toInt()}", fontFamily = FontFamily.Monospace)
                Slider(value = r, onValueChange = { r = it }, valueRange = 0f..255f)
                Text("Green: ${g.toInt()}", fontFamily = FontFamily.Monospace)
                Slider(value = g, onValueChange = { g = it }, valueRange = 0f..255f)
                Text("Blue: ${b.toInt()}", fontFamily = FontFamily.Monospace)
                Slider(value = b, onValueChange = { b = it }, valueRange = 0f..255f)
            }
        },
        confirmButton = {
            TextButton(onClick = {
                if (hexInput.length == 7 && hexInput.startsWith("#")) {
                    onSave(hexInput.uppercase())
                }
            }) {
                Text("[ SAVE ]", fontFamily = FontFamily.Monospace)
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("[ CANCEL ]", fontFamily = FontFamily.Monospace)
            }
        }
    )
}
