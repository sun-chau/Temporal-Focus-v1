package com.example.ui.screens

import android.graphics.Color.parseColor
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
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
import androidx.compose.foundation.isSystemInDarkTheme
import com.example.viewmodel.MainViewModel
import com.example.viewmodel.UiState

data class ThemeInfo(val name: String, val primary: Color, val surface: Color, val background: Color)

fun getPreMadeThemes(isDark: Boolean): List<ThemeInfo> {
    return if (isDark) {
        listOf(
            ThemeInfo("Default", Color(0xFF0A84FF), Color(0xFF1C1C1E), Color(0xFF000000)),
            ThemeInfo("Midnight Minimalist", Color(0xFFFF8C00), Color(0xFF18181B), Color(0xFF09090B)),
            ThemeInfo("Amber Glow", Color(0xFFF59E0B), Color(0xFF2C1A09), Color(0xFF1C0D02)),
            ThemeInfo("Nordic Frost", Color(0xFF38BDF8), Color(0xFF1E293B), Color(0xFF0F172A)),
            ThemeInfo("Forest Canopy", Color(0xFF10B981), Color(0xFF0D5D42), Color(0xFF06402B)),
            ThemeInfo("Crimson Twilight", Color(0xFFE11D48), Color(0xFF4A152C), Color(0xFF2A0A18)),
            ThemeInfo("Monochrome", Color(0xFFE0E0E0), Color(0xFF242424), Color(0xFF121212))
        )
    } else {
        listOf(
            ThemeInfo("Default", Color(0xFF3B82F6), Color(0xFFFFFFFF), Color(0xFFF9FAFB)),
            ThemeInfo("Midnight Minimalist", Color(0xFFEA580C), Color(0xFFFFFFFF), Color(0xFFFAFAFA)),
            ThemeInfo("Amber Glow", Color(0xFFD97706), Color(0xFFFEF3C7), Color(0xFFFFFBEB)),
            ThemeInfo("Nordic Frost", Color(0xFF0284C7), Color(0xFFE0F2FE), Color(0xFFF0F9FF)),
            ThemeInfo("Forest Canopy", Color(0xFF059669), Color(0xFFD1FAE5), Color(0xFFECFDF5)),
            ThemeInfo("Crimson Twilight", Color(0xFFBE123C), Color(0xFFFFE4E6), Color(0xFFFFF1F2)),
            ThemeInfo("Monochrome", Color(0xFF424242), Color(0xFFFFFFFF), Color(0xFFF5F5F5))
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ColorCustomizationScreen(
    viewModel: MainViewModel,
    uiState: UiState,
    onBack: () -> Unit
) {
    var editingParameter by remember { mutableStateOf<String?>(null) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Color Customization") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.surface)
            )
        }
    ) { paddingValues ->
        Box(modifier = Modifier.padding(paddingValues)) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .verticalScroll(rememberScrollState())
            ) {
                // Section 1: Appearance Mode
                Text(
                    text = "APPEARANCE MODE",
                    fontWeight = FontWeight.Bold,
                    style = MaterialTheme.typography.labelLarge,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                )
                
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 8.dp),
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
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
                
                Spacer(Modifier.height(16.dp))
                
                // Section 2: Pre-made Themes
                Text(
                    text = "PRE-MADE THEMES",
                    fontWeight = FontWeight.Bold,
                    style = MaterialTheme.typography.labelLarge,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                )
                
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 12.dp)
                ) {
                    val isSystemDark = isSystemInDarkTheme()
                    val isDark = when (uiState.appearanceMode) {
                        1 -> false
                        2 -> true
                        else -> isSystemDark
                    }
                    val themes = getPreMadeThemes(isDark)
                    
                    for (i in themes.indices step 2) {
                        Row(modifier = Modifier.fillMaxWidth()) {
                            Box(modifier = Modifier.weight(1f)) {
                                ThemeCard(
                                    theme = themes[i],
                                    selected = uiState.currentTheme == themes[i].name,
                                    onClick = { viewModel.setTheme(themes[i].name) }
                                )
                            }
                            if (i + 1 < themes.size) {
                                Box(modifier = Modifier.weight(1f)) {
                                    ThemeCard(
                                        theme = themes[i + 1],
                                        selected = uiState.currentTheme == themes[i + 1].name,
                                        onClick = { viewModel.setTheme(themes[i + 1].name) }
                                    )
                                }
                            } else {
                                Spacer(modifier = Modifier.weight(1f))
                            }
                        }
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
                
                Column(modifier = Modifier.padding(start = 16.dp, end = 16.dp, bottom = 32.dp)) {
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

            if (editingParameter != null) {
                val initialColor = when (editingParameter) {
                    "Backdrop Color" -> uiState.customBackdropColor
                    "Base Text Color" -> uiState.customBaseTextColor
                    "Overdue Text Color" -> uiState.customOverdueTextColor
                    else -> ""
                }
                
                ColorPickerBottomSheet(
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
        Box(
            modifier = Modifier
                .size(32.dp)
                .clip(CircleShape)
                .background(displayColor)
                .border(1.dp, MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f), CircleShape)
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ColorPickerBottomSheet(
    title: String,
    initialHex: String,
    onDismiss: () -> Unit,
    onColorSelected: (String) -> Unit
) {
    var rInput by remember { mutableStateOf("") }
    var gInput by remember { mutableStateOf("") }
    var bInput by remember { mutableStateOf("") }
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
                rInput = android.graphics.Color.red(colorInt).toString()
                gInput = android.graphics.Color.green(colorInt).toString()
                bInput = android.graphics.Color.blue(colorInt).toString()
            } catch (e: Exception) {
                // Ignore parsing error
            }
        }
    }
    
    val updateFromRGB = {
        try {
            val r = rInput.toIntOrNull()?.coerceIn(0, 255) ?: 0
            val g = gInput.toIntOrNull()?.coerceIn(0, 255) ?: 0
            val b = bInput.toIntOrNull()?.coerceIn(0, 255) ?: 0
            val hsv = FloatArray(3)
            android.graphics.Color.colorToHSV(android.graphics.Color.rgb(r, g, b), hsv)
            hue = hsv[0]
            saturation = hsv[1]
            value = hsv[2]
        } catch (e: Exception) {}
    }
    
    val updateFromHSV = {
        val colorInt = android.graphics.Color.HSVToColor(floatArrayOf(hue, saturation, value))
        rInput = android.graphics.Color.red(colorInt).toString()
        gInput = android.graphics.Color.green(colorInt).toString()
        bInput = android.graphics.Color.blue(colorInt).toString()
    }

    ModalBottomSheet(
        onDismissRequest = onDismiss,
        dragHandle = null,
        containerColor = MaterialTheme.colorScheme.surface,
        shape = RoundedCornerShape(topStart = 16.dp, topEnd = 16.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            // 2D Gradient Box (Saturation and Brightness)
            val hueColor = Color.hsv(hue, 1f, 1f)
            BoxWithConstraints(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(200.dp)
                    .clip(RoundedCornerShape(12.dp))
                    .background(
                        Brush.horizontalGradient(
                            colors = listOf(Color.White, hueColor)
                        )
                    )
                    .pointerInput(Unit) {
                        detectDragGestures { change, _ ->
                            change.consume()
                            val width = size.width.toFloat()
                            val height = size.height.toFloat()
                            saturation = (change.position.x / width).coerceIn(0f, 1f)
                            value = 1f - (change.position.y / height).coerceIn(0f, 1f)
                            updateFromHSV()
                        }
                    }
            ) {
                Box(
                    modifier = Modifier
                        .matchParentSize()
                        .background(
                            Brush.verticalGradient(
                                colors = listOf(Color.Transparent, Color.Black)
                            )
                        )
                )
                // Thumb
                val thumbX = saturation
                val thumbY = 1f - value
                val mw = maxWidth
                val mh = maxHeight
                Box(
                    modifier = Modifier.fillMaxSize()
                ) {
                    Box(
                        modifier = Modifier
                            .offset(
                                x = mw * thumbX - 12.dp,
                                y = mh * thumbY - 12.dp
                            )
                            .size(24.dp)
                            .border(2.dp, Color.White, CircleShape)
                    )
                }
            }
            
            Spacer(Modifier.height(16.dp))
            
            // Row with Eyedropper, Preview, and Hue Slider
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    imageVector = Icons.Outlined.Colorize,
                    contentDescription = "Pick color",
                    tint = MaterialTheme.colorScheme.onSurface,
                    modifier = Modifier.size(24.dp)
                )
                Spacer(Modifier.width(16.dp))
                // Color Preview
                Box(
                    modifier = Modifier
                        .size(40.dp)
                        .clip(CircleShape)
                        .background(Color(android.graphics.Color.HSVToColor(floatArrayOf(hue, saturation, value))))
                        .border(1.dp, MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.2f), CircleShape)
                )
                Spacer(Modifier.width(16.dp))
                // Hue Slider
                Box(modifier = Modifier.weight(1f)) {
                    val rainbowColors = listOf(
                        Color.Red, Color.Yellow, Color.Green, Color.Cyan, Color.Blue, Color.Magenta, Color.Red
                    )
                    Slider(
                        value = hue,
                        onValueChange = { 
                            hue = it
                            updateFromHSV()
                        },
                        valueRange = 0f..360f,
                        modifier = Modifier.fillMaxWidth(),
                        colors = SliderDefaults.colors(
                            thumbColor = MaterialTheme.colorScheme.primary,
                            activeTrackColor = Color.Transparent,
                            inactiveTrackColor = Color.Transparent
                        )
                    )
                    Box(
                        modifier = Modifier
                            .matchParentSize()
                            .padding(horizontal = 8.dp)
                            .height(8.dp)
                            .align(Alignment.Center)
                            .clip(RoundedCornerShape(4.dp))
                            .background(Brush.horizontalGradient(rainbowColors))
                    )
                }
            }
            
            Spacer(Modifier.height(24.dp))
            
            // RGB Inputs
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                OutlinedTextField(
                    value = rInput,
                    onValueChange = { rInput = it.take(3); updateFromRGB() },
                    label = { Text("R") },
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                    modifier = Modifier.weight(1f),
                    singleLine = true
                )
                OutlinedTextField(
                    value = gInput,
                    onValueChange = { gInput = it.take(3); updateFromRGB() },
                    label = { Text("G") },
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                    modifier = Modifier.weight(1f),
                    singleLine = true
                )
                OutlinedTextField(
                    value = bInput,
                    onValueChange = { bInput = it.take(3); updateFromRGB() },
                    label = { Text("B") },
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                    modifier = Modifier.weight(1f),
                    singleLine = true
                )
            }
            
            Spacer(Modifier.height(24.dp))
            
            // Action Buttons
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.End
            ) {
                TextButton(onClick = onDismiss) {
                    Text("Cancel", color = MaterialTheme.colorScheme.primary)
                }
                Spacer(Modifier.width(12.dp))
                Button(
                    onClick = {
                        try {
                            val r = rInput.toIntOrNull()?.coerceIn(0, 255) ?: 0
                            val g = gInput.toIntOrNull()?.coerceIn(0, 255) ?: 0
                            val b = bInput.toIntOrNull()?.coerceIn(0, 255) ?: 0
                            val finalHex = String.format("#%02X%02X%02X", r, g, b)
                            onColorSelected(finalHex)
                        } catch (e: Exception) {
                            onDismiss()
                        }
                    },
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
                ) {
                    Text("Apply", color = MaterialTheme.colorScheme.onPrimary)
                }
            }
            Spacer(Modifier.height(16.dp))
        }
    }
}
