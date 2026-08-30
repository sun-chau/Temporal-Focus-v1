import re

with open('app/src/main/java/com/example/ui/screens/ColorCustomizationScreen.kt', 'r') as f:
    content = f.read()

new_content = """package com.example.ui.screens

import android.graphics.Color.parseColor
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.ColorLens
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.outlined.Colorize
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import com.example.viewmodel.MainViewModel
import com.example.viewmodel.UiState

data class ThemeInfo(val name: String, val primary: Color, val surface: Color, val background: Color)

val preMadeThemes = listOf(
    ThemeInfo("Default", Color(0xFF0A84FF), Color(0xFF1C1C1E), Color(0xFF000000)),
    ThemeInfo("Midnight Minimalist", Color(0xFFFF8C00), Color(0xFF18181B), Color(0xFF09090B)),
    ThemeInfo("Amber Glow", Color(0xFFF59E0B), Color(0xFF2C1A09), Color(0xFF1C0D02)),
    ThemeInfo("Nordic Frost", Color(0xFF38BDF8), Color(0xFF1E293B), Color(0xFF0F172A)),
    ThemeInfo("Forest Canopy", Color(0xFF10B981), Color(0xFF0D5D42), Color(0xFF06402B)),
    ThemeInfo("Crimson Twilight", Color(0xFFE11D48), Color(0xFF4A152C), Color(0xFF2A0A18)),
    ThemeInfo("Monochrome", Color(0xFFE0E0E0), Color(0xFF242424), Color(0xFF121212))
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ColorCustomizationBottomSheet(
    viewModel: MainViewModel,
    uiState: UiState,
    onDismiss: () -> Unit
) {
    var editingParameter by remember { mutableStateOf<String?>(null) }

    ModalBottomSheet(
        onDismissRequest = onDismiss,
        dragHandle = { BottomSheetDefaults.DragHandle() },
        modifier = Modifier.fillMaxHeight(0.95f)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .verticalScroll(rememberScrollState())
        ) {
            // Header Section
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 8.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.Top
            ) {
                Row(
                    modifier = Modifier.weight(1f),
                    verticalAlignment = Alignment.Top
                ) {
                    Icon(
                        Icons.Default.ColorLens, 
                        contentDescription = "Palette", 
                        tint = MaterialTheme.colorScheme.primary,
                        modifier = Modifier.padding(top = 4.dp)
                    )
                    Spacer(Modifier.width(12.dp))
                    Text(
                        text = "COLOR CUSTOMIZATION\\nPANEL",
                        fontWeight = FontWeight.Bold,
                        fontFamily = FontFamily.SansSerif,
                        style = MaterialTheme.typography.titleMedium,
                        lineHeight = 20.sp,
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.8f)
                    )
                }
                
                TextButton(
                    onClick = {
                        viewModel.setAppearanceMode(0)
                        viewModel.setTheme("Default")
                    }
                ) {
                    Text("Reset Defaults", color = MaterialTheme.colorScheme.primary)
                }
            }
            
            HorizontalDivider(modifier = Modifier.padding(vertical = 16.dp))
            
            // Section 1: Base Appearance
            Text(
                text = "APPEARANCE",
                fontWeight = FontWeight.Bold,
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
            )
            
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                AppearanceCard(
                    title = "System",
                    selected = uiState.appearanceMode == 0,
                    onClick = { viewModel.setAppearanceMode(0) },
                    modifier = Modifier.weight(1f)
                )
                AppearanceCard(
                    title = "Light",
                    selected = uiState.appearanceMode == 1,
                    onClick = { viewModel.setAppearanceMode(1) },
                    modifier = Modifier.weight(1f)
                )
                AppearanceCard(
                    title = "Dark",
                    selected = uiState.appearanceMode == 2,
                    onClick = { viewModel.setAppearanceMode(2) },
                    modifier = Modifier.weight(1f)
                )
            }
            
            Spacer(Modifier.height(24.dp))
            
            // Section 2: Pre-Made Color Schemes
            Text(
                text = "THEMES",
                fontWeight = FontWeight.Bold,
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
            )
            
            LazyVerticalGrid(
                columns = GridCells.Fixed(2),
                modifier = Modifier
                    .fillMaxWidth()
                    .height(240.dp)
                    .padding(horizontal = 12.dp),
                contentPadding = PaddingValues(bottom = 16.dp)
            ) {
                items(preMadeThemes) { theme ->
                    ThemeCard(
                        theme = theme,
                        selected = uiState.currentTheme == theme.name,
                        onClick = { viewModel.setTheme(theme.name) }
                    )
                }
            }
            
            Spacer(Modifier.height(16.dp))
            
            // Section 3: Custom Color Specifiers
            Text(
                text = "CUSTOM COLOR SPECIFIERS",
                fontWeight = FontWeight.Bold,
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
            )
            
            Column(modifier = Modifier.padding(horizontal = 16.dp, bottom = 32.dp)) {
                CustomColorRow(
                    label = "Backdrop Color",
                    colorHex = uiState.customBackdropColor,
                    onClick = { editingParameter = "Backdrop Color" }
                )
                CustomColorRow(
                    label = "Base Text Color",
                    colorHex = uiState.customBaseTextColor,
                    onClick = { editingParameter = "Base Text Color" }
                )
                CustomColorRow(
                    label = "Overdue Text Color",
                    colorHex = uiState.customOverdueTextColor,
                    onClick = { editingParameter = "Overdue Text Color" }
                )
            }
        }
    }
    
    // Color Picker Dialog
    if (editingParameter != null) {
        val initialColor = when (editingParameter) {
            "Backdrop Color" -> uiState.customBackdropColor
            "Base Text Color" -> uiState.customBaseTextColor
            "Overdue Text Color" -> uiState.customOverdueTextColor
            else -> ""
        }
        
        ColorPickerDialog(
            title = editingParameter!!,
            initialHex = initialColor,
            onDismiss = { editingParameter = null },
            onColorSelected = { newHex ->
                val backdrop = if (editingParameter == "Backdrop Color") newHex else uiState.customBackdropColor
                val baseText = if (editingParameter == "Base Text Color") newHex else uiState.customBaseTextColor
                val overdueText = if (editingParameter == "Overdue Text Color") newHex else uiState.customOverdueTextColor
                viewModel.setCustomColors(backdrop, baseText, overdueText)
                editingParameter = null
            }
        )
    }
}

@Composable
fun AppearanceCard(title: String, selected: Boolean, onClick: () -> Unit, modifier: Modifier = Modifier) {
    Card(
        modifier = modifier.clickable(onClick = onClick),
        shape = RoundedCornerShape(12.dp),
        border = if (selected) BorderStroke(2.dp, MaterialTheme.colorScheme.primary) else BorderStroke(1.dp, MaterialTheme.colorScheme.surfaceVariant),
        colors = CardDefaults.cardColors(
            containerColor = if (selected) MaterialTheme.colorScheme.primary.copy(alpha = 0.1f) else MaterialTheme.colorScheme.surface
        )
    ) {
        Box(modifier = Modifier.fillMaxWidth().padding(vertical = 12.dp), contentAlignment = Alignment.Center) {
            Text(
                text = title,
                fontWeight = if (selected) FontWeight.Bold else FontWeight.Normal,
                color = if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface
            )
        }
    }
}

@Composable
fun ThemeCard(theme: ThemeInfo, selected: Boolean, onClick: () -> Unit) {
    Card(
        modifier = Modifier
            .padding(4.dp)
            .clickable(onClick = onClick),
        shape = RoundedCornerShape(12.dp),
        border = if (selected) BorderStroke(2.dp, MaterialTheme.colorScheme.primary) else BorderStroke(1.dp, MaterialTheme.colorScheme.surfaceVariant),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
    ) {
        Column(modifier = Modifier.padding(12.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = theme.name,
                    style = MaterialTheme.typography.bodyMedium,
                    fontWeight = if (selected) FontWeight.Bold else FontWeight.Normal,
                    color = MaterialTheme.colorScheme.onSurface,
                    modifier = Modifier.weight(1f)
                )
                if (selected) {
                    Icon(
                        Icons.Default.CheckCircle,
                        contentDescription = "Selected",
                        tint = MaterialTheme.colorScheme.primary,
                        modifier = Modifier.size(16.dp)
                    )
                }
            }
            Spacer(Modifier.height(12.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Box(modifier = Modifier.size(24.dp).clip(CircleShape).background(theme.primary))
                Box(modifier = Modifier.size(24.dp).clip(CircleShape).background(theme.surface))
                Box(modifier = Modifier.size(24.dp).clip(CircleShape).background(theme.background).border(1.dp, Color.Gray, CircleShape))
            }
        }
    }
}

@Composable
fun CustomColorRow(label: String, colorHex: String, onClick: () -> Unit) {
    val displayColor = try {
        if (colorHex.isNotEmpty()) Color(parseColor(colorHex)) else Color.Transparent
    } catch (e: Exception) {
        Color.Transparent
    }

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
            .padding(vertical = 12.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(text = label, style = MaterialTheme.typography.bodyLarge)
        Row(verticalAlignment = Alignment.CenterVertically) {
            if (colorHex.isNotEmpty()) {
                Text(
                    text = colorHex.uppercase(),
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.padding(end = 8.dp)
                )
            } else {
                Text(
                    text = "Not Set",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f),
                    modifier = Modifier.padding(end = 8.dp)
                )
            }
            Box(
                modifier = Modifier
                    .size(32.dp)
                    .clip(CircleShape)
                    .background(displayColor)
                    .border(1.dp, MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.3f), CircleShape)
            )
        }
    }
}

@Composable
fun ColorPickerDialog(
    title: String,
    initialHex: String,
    onDismiss: () -> Unit,
    onColorSelected: (String) -> Unit
) {
    var hexInput by remember { mutableStateOf(initialHex.replace("#", "")) }
    var hue by remember { mutableStateOf(0f) }
    var saturation by remember { mutableStateOf(1f) }
    var value by remember { mutableStateOf(1f) }

    LaunchedEffect(initialHex) {
        if (initialHex.isNotEmpty()) {
            try {
                val colorInt = android.graphics.Color.parseColor(if (initialHex.startsWith("#")) initialHex else "#$initialHex")
                val hsv = FloatArray(3)
                android.graphics.Color.colorToHSV(colorInt, hsv)
                hue = hsv[0]
                saturation = hsv[1]
                value = hsv[2]
            } catch (e: Exception) {
                // Ignore parsing error
            }
        }
    }

    Dialog(onDismissRequest = onDismiss) {
        Card(
            shape = RoundedCornerShape(24.dp),
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
        ) {
            Column(modifier = Modifier.padding(24.dp)) {
                Text(
                    text = "Set $title",
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(bottom = 16.dp)
                )
                
                // Color Preview
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(60.dp)
                        .clip(RoundedCornerShape(12.dp))
                        .background(Color(android.graphics.Color.HSVToColor(floatArrayOf(hue, saturation, value))))
                        .border(1.dp, MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.2f), RoundedCornerShape(12.dp))
                )
                
                Spacer(Modifier.height(24.dp))
                
                // Hue Slider
                Text("Hue", style = MaterialTheme.typography.labelMedium)
                Slider(
                    value = hue,
                    onValueChange = { 
                        hue = it
                        hexInput = String.format("%06X", (0xFFFFFF and android.graphics.Color.HSVToColor(floatArrayOf(hue, saturation, value))))
                    },
                    valueRange = 0f..360f,
                    modifier = Modifier.fillMaxWidth()
                )
                
                // Saturation Slider
                Text("Saturation", style = MaterialTheme.typography.labelMedium)
                Slider(
                    value = saturation,
                    onValueChange = { 
                        saturation = it
                        hexInput = String.format("%06X", (0xFFFFFF and android.graphics.Color.HSVToColor(floatArrayOf(hue, saturation, value))))
                    },
                    valueRange = 0f..1f,
                    modifier = Modifier.fillMaxWidth()
                )
                
                // Value Slider
                Text("Brightness", style = MaterialTheme.typography.labelMedium)
                Slider(
                    value = value,
                    onValueChange = { 
                        value = it
                        hexInput = String.format("%06X", (0xFFFFFF and android.graphics.Color.HSVToColor(floatArrayOf(hue, saturation, value))))
                    },
                    valueRange = 0f..1f,
                    modifier = Modifier.fillMaxWidth()
                )
                
                Spacer(Modifier.height(16.dp))
                
                OutlinedTextField(
                    value = hexInput,
                    onValueChange = { 
                        hexInput = it.take(6).uppercase()
                        if (hexInput.length == 6) {
                            try {
                                val colorInt = android.graphics.Color.parseColor("#$hexInput")
                                val hsv = FloatArray(3)
                                android.graphics.Color.colorToHSV(colorInt, hsv)
                                hue = hsv[0]
                                saturation = hsv[1]
                                value = hsv[2]
                            } catch (e: Exception) {
                                // Ignore error while typing
                            }
                        }
                    },
                    label = { Text("Hex Code") },
                    prefix = { Text("#") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
                
                Spacer(Modifier.height(24.dp))
                
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.End
                ) {
                    TextButton(onClick = onDismiss) {
                        Text("Cancel")
                    }
                    Spacer(Modifier.width(8.dp))
                    Button(onClick = {
                        val finalHex = if (hexInput.length == 6) "#$hexInput" else ""
                        if (finalHex.isNotEmpty()) {
                            onColorSelected(finalHex)
                        } else {
                            onDismiss()
                        }
                    }) {
                        Text("Save")
                    }
                }
            }
        }
    }
}
"""

with open('app/src/main/java/com/example/ui/screens/ColorCustomizationScreen.kt', 'w') as f:
    f.write(new_content)
