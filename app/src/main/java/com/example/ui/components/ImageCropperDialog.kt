package com.example.ui.components

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Matrix
import android.net.Uri
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectTransformGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Rect
import androidx.compose.ui.graphics.*
import androidx.compose.ui.graphics.drawscope.clipPath
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.IntSize
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File
import java.io.FileOutputStream
import kotlin.math.max

@Composable
fun ImageCropperDialog(
    uri: Uri,
    onDismiss: () -> Unit,
    onCropped: (Uri) -> Unit
) {
    val context = LocalContext.current
    var bitmap by remember { mutableStateOf<Bitmap?>(null) }
    var containerSize by remember { mutableStateOf(IntSize.Zero) }

    var scale by remember { mutableFloatStateOf(1f) }
    var offset by remember { mutableStateOf(Offset.Zero) }

    LaunchedEffect(uri) {
        withContext(Dispatchers.IO) {
            try {
                val inputStream = context.contentResolver.openInputStream(uri)
                val originalBitmap = BitmapFactory.decodeStream(inputStream)
                inputStream?.close()

                var rotatedBitmap = originalBitmap
                val exifStream = context.contentResolver.openInputStream(uri)
                if (exifStream != null && originalBitmap != null) {
                    val exif = android.media.ExifInterface(exifStream)
                    val orientation = exif.getAttributeInt(
                        android.media.ExifInterface.TAG_ORIENTATION,
                        android.media.ExifInterface.ORIENTATION_NORMAL
                    )

                    val matrix = android.graphics.Matrix()
                    when (orientation) {
                        android.media.ExifInterface.ORIENTATION_ROTATE_90 -> matrix.postRotate(90f)
                        android.media.ExifInterface.ORIENTATION_ROTATE_180 -> matrix.postRotate(180f)
                        android.media.ExifInterface.ORIENTATION_ROTATE_270 -> matrix.postRotate(270f)
                        android.media.ExifInterface.ORIENTATION_FLIP_HORIZONTAL -> matrix.postScale(-1f, 1f)
                        android.media.ExifInterface.ORIENTATION_FLIP_VERTICAL -> {
                            matrix.postRotate(180f)
                            matrix.postScale(-1f, 1f)
                        }
                        android.media.ExifInterface.ORIENTATION_TRANSPOSE -> {
                            matrix.postRotate(90f)
                            matrix.postScale(-1f, 1f)
                        }
                        android.media.ExifInterface.ORIENTATION_TRANSVERSE -> {
                            matrix.postRotate(-90f)
                            matrix.postScale(-1f, 1f)
                        }
                    }

                    if (!matrix.isIdentity) {
                        rotatedBitmap = android.graphics.Bitmap.createBitmap(
                            originalBitmap, 0, 0, originalBitmap.width, originalBitmap.height, matrix, true
                        )
                        if (rotatedBitmap != originalBitmap) {
                            originalBitmap.recycle()
                        }
                    }
                    exifStream.close()
                }

                bitmap = rotatedBitmap
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false, dismissOnBackPress = true, dismissOnClickOutside = false)
    ) {
        Surface(
            modifier = Modifier.fillMaxSize(),
            color = MaterialTheme.colorScheme.background
        ) {
            Column(modifier = Modifier.fillMaxSize().systemBarsPadding()) {
                // Top Bar
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        IconButton(onClick = onDismiss) {
                            Icon(Icons.Default.Close, contentDescription = "Close", tint = MaterialTheme.colorScheme.onBackground)
                        }
                        Text("Drag the image to adjust", color = MaterialTheme.colorScheme.onBackground, fontSize = 16.sp)
                    }
                    TextButton(onClick = { /* trigger photo picker again */ onDismiss() }) {
                        Text("Upload", color = MaterialTheme.colorScheme.onBackground)
                    }
                }

                Box(
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxWidth()
                        .clipToBounds()
                        .background(Color.Black)
                        
                        .onSizeChanged { containerSize = it }
                        .pointerInput(Unit) {
                            detectTransformGestures { _, pan, zoom, _ ->
                                scale = (scale * zoom).coerceIn(0.5f, 5f)
                                offset += pan
                            }
                        }
                ) {
                    bitmap?.let { b ->
                        val imageRatio = b.width.toFloat() / b.height.toFloat()
                        val containerRatio = if (containerSize.height > 0) containerSize.width.toFloat() / containerSize.height.toFloat() else 1f

                        val fitScale = if (imageRatio > containerRatio) {
                            containerSize.width.toFloat() / b.width.toFloat()
                        } else {
                            containerSize.height.toFloat() / b.height.toFloat()
                        }

                        val drawWidth = b.width * fitScale
                        val drawHeight = b.height * fitScale

                        val imageBitmap = b.asImageBitmap()

                        Canvas(modifier = Modifier.fillMaxSize()) {
                            val circleRadius = minOf(size.width, size.height) * 0.45f
                            val center = Offset(size.width / 2, size.height / 2)

                            // Calculate image bounds
                            val left = center.x - drawWidth / 2f * scale + offset.x
                            val top = center.y - drawHeight / 2f * scale + offset.y

                            // Draw image
                            drawImage(
                                image = imageBitmap,
                                dstOffset = androidx.compose.ui.unit.IntOffset(left.toInt(), top.toInt()),
                                dstSize = IntSize((drawWidth * scale).toInt(), (drawHeight * scale).toInt())
                            )

                            // Draw overlay
                            val path = Path().apply {
                                addRect(Rect(0f, 0f, size.width, size.height))
                                addRect(Rect(center.x - circleRadius, center.y - circleRadius, center.x + circleRadius, center.y + circleRadius))
                                fillType = PathFillType.EvenOdd
                            }
                            drawPath(path = path, color = Color.Black.copy(alpha = 0.6f))
                        }
                    }

                    // Zoom controls
                    Column(
                        modifier = Modifier
                            .align(Alignment.CenterEnd)
                            .padding(end = 16.dp)
                            .clip(RoundedCornerShape(8.dp))
                            .background(Color.DarkGray.copy(alpha = 0.5f))
                    ) {
                        TextButton(onClick = { scale = (scale + 0.2f).coerceAtMost(5f) }) { Text("+", color = Color.White, fontSize = 20.sp) }
                        TextButton(onClick = { scale = (scale - 0.2f).coerceAtLeast(0.5f) }) { Text("-", color = Color.White, fontSize = 24.sp) }
                    }

                    // Confirm button
                    FloatingActionButton(
                        onClick = {
                            bitmap?.let { b ->
                                // Calculate the crop rect
                                val circleRadius = minOf(containerSize.width, containerSize.height) * 0.45f
                                val center = Offset(containerSize.width / 2f, containerSize.height / 2f)

                                val fitScale = if (b.width.toFloat() / b.height > containerSize.width.toFloat() / containerSize.height) {
                                    containerSize.width.toFloat() / b.width
                                } else {
                                    containerSize.height.toFloat() / b.height
                                }

                                val displayedWidth = b.width * fitScale * scale
                                val displayedHeight = b.height * fitScale * scale

                                val leftOffset = center.x - displayedWidth / 2f + offset.x
                                val topOffset = center.y - displayedHeight / 2f + offset.y

                                val cropLeft = ((center.x - circleRadius - leftOffset) / (fitScale * scale)).coerceIn(0f, b.width.toFloat())
                                val cropTop = ((center.y - circleRadius - topOffset) / (fitScale * scale)).coerceIn(0f, b.height.toFloat())
                                val cropRight = ((center.x + circleRadius - leftOffset) / (fitScale * scale)).coerceIn(0f, b.width.toFloat())
                                val cropBottom = ((center.y + circleRadius - topOffset) / (fitScale * scale)).coerceIn(0f, b.height.toFloat())

                                val cropWidth = (cropRight - cropLeft).coerceAtLeast(1f).toInt()
                                val cropHeight = (cropBottom - cropTop).coerceAtLeast(1f).toInt()

                                val cropped = Bitmap.createBitmap(b, cropLeft.toInt(), cropTop.toInt(), cropWidth, cropHeight)
                                
                                val file = File(context.filesDir, "cropped_profile_${System.currentTimeMillis()}.jpg")
                                val out = FileOutputStream(file)
                                cropped.compress(Bitmap.CompressFormat.JPEG, 90, out)
                                out.flush()
                                out.close()
                                
                                onCropped(Uri.fromFile(file))
                            }
                        },
                        modifier = Modifier
                            .align(Alignment.BottomEnd)
                            .padding(end = 24.dp, bottom = 80.dp),
                        containerColor = MaterialTheme.colorScheme.primary,
                        contentColor = MaterialTheme.colorScheme.onPrimary
                    ) {
                        Icon(Icons.Default.Check, contentDescription = "Done")
                    }
                }
            }
        }
    }
}
