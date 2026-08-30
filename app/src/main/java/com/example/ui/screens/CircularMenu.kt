package com.example.ui.screens

import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.FastForward
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material.icons.outlined.MoreVert
import androidx.compose.material.icons.outlined.*
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Popup
import androidx.compose.ui.window.PopupProperties
import kotlin.math.cos
import kotlin.math.sin

@Composable
fun CircularMenu(
    isOverdue: Boolean,
    onComplete: () -> Unit,
    onEdit: () -> Unit,
    onInfo: () -> Unit,
    onDelete: () -> Unit,
    onShift: (() -> Unit)? = null
) {
    var expanded by remember { mutableStateOf(false) }
    val transition = updateTransition(targetState = expanded, label = "menuTransition")
    val context = androidx.compose.ui.platform.LocalContext.current
    
    val animationProgress by transition.animateFloat(
        transitionSpec = { spring(dampingRatio = Spring.DampingRatioMediumBouncy, stiffness = Spring.StiffnessLow) },
        label = "progress"
    ) { if (it) 1f else 0f }

    Box(contentAlignment = Alignment.Center) {
        if (expanded || animationProgress > 0f) {
            Popup(
                alignment = Alignment.TopEnd,
                onDismissRequest = { expanded = false },
                properties = PopupProperties(focusable = true)
            ) {
                Box(
                    modifier = Modifier.size(240.dp).offset(x = 16.dp, y = (-16).dp),
                    contentAlignment = Alignment.TopEnd
                ) {
                    val radius = 100.dp.value
                    
                    val items = mutableListOf(
                        Triple(Icons.Outlined.Check, onComplete, MaterialTheme.colorScheme.primary),
                        Triple(Icons.Outlined.Edit, onEdit, MaterialTheme.colorScheme.onSurface),
                        Triple(Icons.Outlined.Info, onInfo, MaterialTheme.colorScheme.onSurface)
                    )
                    if (onShift != null) {
                        items.add(Triple(Icons.Default.FastForward, onShift, if (isOverdue) Color(0xFF03A9F4) else Color(0xFF03A9F4).copy(alpha = 0.4f)))
                    }
                    items.add(Triple(Icons.Outlined.Delete, onDelete, MaterialTheme.colorScheme.error))

                    items.forEachIndexed { index, (icon, action, color) ->
                        // Angle from 75 to 195 degrees
                        val angleDegrees = 75.0 + (120.0 / (items.size - 1)) * index
                        val angleRad = Math.toRadians(angleDegrees)
                        
                        val xOffset = (radius * cos(angleRad) * animationProgress).dp
                        val yOffset = (radius * sin(angleRad) * animationProgress).dp
                        
                        IconButton(
                            onClick = { 
                                 if (icon == Icons.Default.FastForward && !isOverdue) {
                                    android.widget.Toast.makeText(context, "Still some time left, wait.", android.widget.Toast.LENGTH_SHORT).show()
                                    expanded = false
                                } else {
                                    action()
                                    expanded = false 
                                }
                             },
                            modifier = Modifier
                                .offset(x = xOffset, y = yOffset)
                                .size(48.dp)
                                .clip(CircleShape)
                                .background(MaterialTheme.colorScheme.surfaceVariant)
                        ) {
                            Icon(icon, contentDescription = null, tint = color)
                        }
                    }

                    // Center close button
                    IconButton(
                        onClick = { expanded = false },
                        modifier = Modifier
                            .size(32.dp)
                            .clip(CircleShape)
                            .background(Color(0xFF444444))
                    ) {
                        Icon(Icons.Outlined.Close, contentDescription = "Close", tint = MaterialTheme.colorScheme.onSurface)
                    }
                }
            }
        } else {
            IconButton(
                onClick = { expanded = true },
                modifier = Modifier
                    .size(32.dp)
                    .clip(CircleShape)
                    .background(MaterialTheme.colorScheme.surfaceVariant)
            ) {
                Icon(Icons.Outlined.MoreVert, contentDescription = "Options", tint = MaterialTheme.colorScheme.onSurface)
            }
        }
    }
}
