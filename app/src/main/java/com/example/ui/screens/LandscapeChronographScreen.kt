package com.example.ui.screens

import android.app.Activity
import android.content.pm.ActivityInfo
import android.os.Build
import android.view.WindowManager
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.DarkMode
import androidx.compose.material.icons.filled.LightMode
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalView
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import androidx.compose.ui.window.DialogWindowProvider
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat
import com.example.viewmodel.MainViewModel
import com.example.viewmodel.UiState
import kotlinx.coroutines.delay
import java.text.SimpleDateFormat
import java.util.*
import kotlin.random.Random

@OptIn(ExperimentalFoundationApi::class)
@Composable
fun LandscapeChronographScreen(
    viewModel: MainViewModel,
    uiState: UiState,
    onBack: () -> Unit
) {
    val context = LocalContext.current
    val activity = context as? Activity
    
    Dialog(
        onDismissRequest = onBack,
        properties = DialogProperties(
            usePlatformDefaultWidth = false,
            dismissOnBackPress = true,
            decorFitsSystemWindows = false
        )
    ) {
        val view = LocalView.current
        
        DisposableEffect(view) {
            val window = (view.parent as? DialogWindowProvider)?.window ?: activity?.window
            activity?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
            window?.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
            
            window?.let { win ->
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
                    win.attributes = win.attributes.apply {
                        layoutInDisplayCutoutMode = WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES
                    }
                }
                WindowInsetsControllerCompat(win, win.decorView).apply {
                    hide(WindowInsetsCompat.Type.systemBars())
                    systemBarsBehavior = WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
                }
                win.setBackgroundDrawableResource(android.R.color.transparent)
            }
            
            onDispose {
                activity?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED
                window?.clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
                window?.let { win ->
                    WindowInsetsControllerCompat(win, win.decorView).apply {
                        show(WindowInsetsCompat.Type.systemBars())
                    }
                }
            }
        }

        var isDarkMode by remember { mutableStateOf(true) }
        var isUtilityMode by remember { mutableStateOf(false) }
        var is24HourFormat by remember { mutableStateOf(true) }
        var controlsVisible by remember { mutableStateOf(true) }
        
        // Auto-hide controls
        LaunchedEffect(controlsVisible) {
            if (controlsVisible) {
                delay(4000L)
                controlsVisible = false
            }
        }
        
        // Burn-in protection offsets
        var timeOffsetX by remember { mutableStateOf(0) }
        var timeOffsetY by remember { mutableStateOf(0) }
        var iconOffsetX by remember { mutableStateOf(0) }
        var iconOffsetY by remember { mutableStateOf(0) }

        LaunchedEffect(Unit) {
            while(true) {
                delay(60000L) // every 60 seconds
                timeOffsetX = Random.nextInt(-20, 20)
                timeOffsetY = Random.nextInt(-20, 20)
                iconOffsetX = Random.nextInt(-10, 10)
                iconOffsetY = Random.nextInt(-10, 10)
            }
        }

        val backgroundColor by animateColorAsState(
            targetValue = when {
                isDarkMode -> Color(0xFF000000)
                isUtilityMode -> Color(0xFFF4ECD8) // Sepia
                else -> Color(0xFFFFFFFF)
            },
            animationSpec = tween(500)
        )
        val textColor by animateColorAsState(
            targetValue = when {
                isDarkMode && isUtilityMode -> Color(0xFFFF3333) // Deep Red
                isDarkMode -> Color(0xFFFFFFFF)
                isUtilityMode -> Color(0xFF3E2723) // Deep Brown
                else -> Color(0xFF000000)
            },
            animationSpec = tween(500)
        )

        val currentTime = Date(uiState.currentDateTime)
        
        val timePattern = if (is24HourFormat) "HH:mm:ss" else "hh:mm:ss"
        val timePatternReal = if (uiState.use24HourFormat) timePattern.replace("hh", "HH").replace("h", "H") else timePattern
        val timeFormatter = SimpleDateFormat(timePatternReal, Locale.getDefault())
        val timeDigits = timeFormatter.format(currentTime)
        
        val meridiemFormatter = SimpleDateFormat("a", Locale.getDefault())
        val meridiemText = if (is24HourFormat) "" else meridiemFormatter.format(currentTime)
        
        val dateFormatter = SimpleDateFormat("EEEE, MMMM d, yyyy", Locale.getDefault())
        val formattedDate = dateFormatter.format(currentTime)

        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(backgroundColor)
                .pointerInput(Unit) {
                    detectTapGestures(
                        onTap = { controlsVisible = !controlsVisible },
                        onLongPress = { isUtilityMode = !isUtilityMode }
                    )
                }
        ) {
            // Main Stage
            Column(
                modifier = Modifier
                    .align(Alignment.Center)
                    .offset { IntOffset(timeOffsetX, timeOffsetY) },
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.Center
                ) {
                    Text(
                        text = timeDigits,
                        fontSize = 110.sp,
                        fontWeight = FontWeight.Bold,
                        fontFamily = FontFamily.Monospace,
                        color = textColor,
                        maxLines = 1
                    )
                    if (!is24HourFormat) {
                        Spacer(modifier = Modifier.width(12.dp))
                        Text(
                            text = meridiemText.lowercase(Locale.getDefault()),
                            fontSize = 36.sp,
                            fontWeight = FontWeight.Medium,
                            fontFamily = FontFamily.Monospace,
                            color = textColor.copy(alpha = 0.75f),
                            modifier = Modifier
                                .align(Alignment.Bottom)
                                .padding(bottom = 20.dp)
                        )
                    }
                }
                Text(
                    text = formattedDate,
                    fontSize = 32.sp,
                    fontWeight = FontWeight.Medium,
                    fontFamily = FontFamily.Monospace,
                    color = textColor.copy(alpha = 0.8f)
                )
            }

            // Top Left: Close
            AnimatedVisibility(
                visible = controlsVisible,
                enter = fadeIn(),
                exit = fadeOut(),
                modifier = Modifier.align(Alignment.TopStart)
            ) {
                IconButton(
                    onClick = onBack,
                    modifier = Modifier
                        .windowInsetsPadding(WindowInsets.safeDrawing)
                        .padding(24.dp)
                        .offset { IntOffset(iconOffsetX, iconOffsetY) }
                ) {
                    Icon(
                        imageVector = Icons.Default.Close,
                        contentDescription = "Close",
                        tint = Color.Red,
                        modifier = Modifier.size(32.dp)
                    )
                }
            }

            // Bottom Left: Theme & Format Toggle
            AnimatedVisibility(
                visible = controlsVisible,
                enter = fadeIn(),
                exit = fadeOut(),
                modifier = Modifier.align(Alignment.BottomStart)
            ) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier
                        .windowInsetsPadding(WindowInsets.safeDrawing)
                        .padding(24.dp)
                        .offset { IntOffset(iconOffsetX, iconOffsetY) }
                ) {
                    IconButton(
                        onClick = {
                            isDarkMode = !isDarkMode
                            isUtilityMode = false
                        }
                    ) {
                        Icon(
                            imageVector = if (isDarkMode) Icons.Default.LightMode else Icons.Default.DarkMode,
                            contentDescription = "Toggle Theme",
                            tint = textColor,
                            modifier = Modifier.size(32.dp)
                        )
                    }
                    Spacer(modifier = Modifier.width(16.dp))
                    Box(
                        modifier = Modifier
                            .clip(CircleShape)
                            .border(
                                1.dp, 
                                textColor.copy(alpha = 0.5f), 
                                CircleShape
                            )
                            .clickable { 
                                is24HourFormat = !is24HourFormat
                                controlsVisible = true // Reset timer on click
                            }
                            .padding(horizontal = 16.dp, vertical = 8.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = if (is24HourFormat) "24" else "12",
                            color = textColor,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }
            }
        }
    }
}
