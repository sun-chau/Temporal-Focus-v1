package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.outlined.Info
import androidx.compose.material.icons.outlined.Notifications
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.DateRange
import androidx.compose.material.icons.filled.ArrowDropDown
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.AttachFile
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.viewmodel.MainViewModel
import com.example.ui.utils.getLabelColor
import com.example.ui.utils.getLabelName
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import com.example.data.RecurrenceType

import com.example.ui.screens.getDayOfWeekName
import com.example.ui.screens.getWeekName
import com.example.ui.screens.getMonthName
import com.example.ui.screens.parseDateString
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.ui.text.style.TextAlign
import java.util.Calendar
import com.example.data.MonthlyType
import com.example.data.AnnuallyType


import androidx.compose.material.icons.filled.AddLink

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CreateChronometerScreen(viewModel: MainViewModel) {
    val uiState by viewModel.uiState.collectAsState()
    val keyboardController = androidx.compose.ui.platform.LocalSoftwareKeyboardController.current
    val editingTask = uiState.editingTask
    var name by remember { mutableStateOf(editingTask?.name ?: "") }
    var description by remember { mutableStateOf(editingTask?.description ?: "") }
    var link by remember { mutableStateOf(editingTask?.link ?: "") }
    var attachmentUri by remember { mutableStateOf(editingTask?.attachmentUri ?: "") }
    
    var showLinkDialog by remember { mutableStateOf(false) }
    
    // Tags
    val availableTags = uiState.customLabels.toList()
    var selectedTags by remember { mutableStateOf(if (editingTask?.labels?.isNotEmpty() == true) editingTask.labels.split(",").toSet() else setOf<String>()) }
    
    // Time & Date
    var createdAt by remember { mutableStateOf(editingTask?.createdAt ?: System.currentTimeMillis()) }
    var targetTime by remember { mutableStateOf(editingTask?.targetDateTime ?: (System.currentTimeMillis() + 86400000L)) } // +1 day
    var priority by remember { mutableStateOf(editingTask?.priority ?: "Normal") }
    var deadlineDateTime by remember { mutableStateOf<Long?>(editingTask?.deadlineDateTime) }
    
    var showCreatedPicker by remember { mutableStateOf(false) }
    var showTargetPicker by remember { mutableStateOf(false) }
    var showPriorityMenu by remember { mutableStateOf(false) }
    var showDeadlineMenu by remember { mutableStateOf(false) }
    var showCustomDeadlinePicker by remember { mutableStateOf(false) }
    
    // Recurring
    var isRecurring by remember { mutableStateOf(false) }
    var recurrenceType by remember { mutableStateOf(RecurrenceType.MONTHLY) }
    
    var monthlyType by remember { mutableStateOf(MonthlyType.DATES) }
    var monthlyDates by remember { mutableStateOf(setOf<Int>()) }
    var monthlyWeek by remember { mutableStateOf(1) }
    var monthlyDayOfWeek by remember { mutableStateOf(Calendar.SUNDAY) }

    var annuallyType by remember { mutableStateOf(AnnuallyType.DATES) }
    var annuallyMonth by remember { mutableStateOf(Calendar.JANUARY) }
    var annuallyDates by remember { mutableStateOf(setOf<Int>()) }
    var annuallyWeek by remember { mutableStateOf(1) }
    var annuallyDayOfWeek by remember { mutableStateOf(Calendar.SUNDAY) }
    
    var occurrenceCount by remember { mutableStateOf(1) }
    
    var minusHolding by remember { mutableStateOf(false) }
    var plusHolding by remember { mutableStateOf(false) }

    LaunchedEffect(minusHolding) {
        if (minusHolding) {
            if (occurrenceCount > 0) occurrenceCount--
            kotlinx.coroutines.delay(500)
            while (minusHolding && occurrenceCount > 0) {
                occurrenceCount--
                kotlinx.coroutines.delay(100)
            }
        }
    }

    LaunchedEffect(plusHolding) {
        if (plusHolding) {
            occurrenceCount++
            kotlinx.coroutines.delay(500)
            while (plusHolding) {
                occurrenceCount++
                kotlinx.coroutines.delay(100)
            }
        }
    }
    
    val dynamicString = remember(
        isRecurring, recurrenceType,
        monthlyType, monthlyDates, monthlyWeek, monthlyDayOfWeek,
        annuallyType, annuallyMonth, annuallyDates, annuallyWeek, annuallyDayOfWeek, occurrenceCount
    ) {
        if (!isRecurring) return@remember "Does not repeat"
        
        val countStr = if (occurrenceCount <= 0) " indefinitely." else if (occurrenceCount > 1) " for $occurrenceCount occurrences." else " once."
        
        when (recurrenceType) {
            RecurrenceType.MONTHLY -> {
                val condition = when (monthlyType) {
                    MonthlyType.DATES -> {
                        if (monthlyDates.isEmpty()) "no dates"
                        else "dates ${monthlyDates.sorted().joinToString(", ")}"
                    }
                    MonthlyType.LAST_DAY -> "the last day of the month"
                    MonthlyType.DAY_OF_WEEK -> {
                        val weekName = getWeekName(monthlyWeek)
                        val dayName = getDayOfWeekName(monthlyDayOfWeek)
                        "the $weekName $dayName"
                    }
                }
                "Repeats every month on $condition$countStr"
            }
            RecurrenceType.ANNUALLY -> {
                val monthName = getMonthName(annuallyMonth)
                val condition = when (annuallyType) {
                    AnnuallyType.DATES -> {
                        if (annuallyDates.isEmpty()) "no dates"
                        else "dates ${annuallyDates.sorted().joinToString(", ")} of $monthName"
                    }
                    AnnuallyType.END_OF_YEAR -> "the end of the year (Dec 31)"
                    AnnuallyType.DAY_OF_WEEK -> {
                        val weekName = getWeekName(annuallyWeek)
                        val dayName = getDayOfWeekName(annuallyDayOfWeek)
                        "the $weekName $dayName of $monthName"
                    }
                }
                "Repeats annually on $condition$countStr"
            }
            else -> "Does not repeat"
        }
    }
    
    val formatDateTime = { time: Long ->
        SimpleDateFormat(if (uiState.use24HourFormat) "dd-MM-yyyy HH:mm" else "dd-MM-yyyy hh:mm a", Locale.getDefault()).format(Date(time))
    }
    
    val context = androidx.compose.ui.platform.LocalContext.current
    val filePickerLauncher = androidx.activity.compose.rememberLauncherForActivityResult(
        contract = androidx.activity.result.contract.ActivityResultContracts.OpenDocument()
    ) { uri: android.net.Uri? ->
        uri?.let {
            try {
                context.contentResolver.takePersistableUriPermission(
                    it, 
                    android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION
                )
                attachmentUri = it.toString()
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
    
    if (showTargetPicker) {
        DateTimePickerDialog(
            initialTime = targetTime,
            use24HourFormat = uiState.use24HourFormat,
            onDismiss = { showTargetPicker = false },
            onTimeSelected = { 
                targetTime = it
                showTargetPicker = false
            }
        )
    }

    if (showLinkDialog) {
        var tempLink by remember { mutableStateOf(link) }
        AlertDialog(
            onDismissRequest = { showLinkDialog = false },
            title = { Text("Add Link") },
            text = {
                OutlinedTextField(
                    value = tempLink,
                    onValueChange = { tempLink = it },
                    placeholder = { Text("example.com") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
            },
            confirmButton = {
                TextButton(onClick = { 
                    var finalLink = tempLink.trim()
                    if (finalLink.isNotEmpty() && !finalLink.startsWith("http://") && !finalLink.startsWith("https://")) {
                        finalLink = "https://$finalLink"
                    }
                    link = finalLink
                    showLinkDialog = false 
                }) {
                    Text("Save")
                }
            },
            dismissButton = {
                TextButton(onClick = { showLinkDialog = false }) {
                    Text("Cancel")
                }
            }
        )
    }
    
    if (showCreatedPicker) {
        DateTimePickerDialog(
            initialTime = createdAt,
            use24HourFormat = uiState.use24HourFormat,
            onDismiss = { showCreatedPicker = false },
            onTimeSelected = { 
                createdAt = it
                showCreatedPicker = false
            }
        )
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
    ) {
        // Header
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(onClick = { viewModel.setEditingTask(null)
                    viewModel.setCreatingChronometer(false) }, modifier = Modifier.size(48.dp)) {
                Icon(Icons.Default.Close, contentDescription = "Close", tint = MaterialTheme.colorScheme.onSurface)
            }
            IconButton(
                onClick = { 
                                        viewModel.saveAdvancedDeadline(
                        com.example.data.DeadlineDraft(
                            name = if (name.isBlank()) "Untitled Task" else name,
                            description = description.takeIf { it.isNotBlank() },
                            labels = selectedTags.joinToString(","),
                            targetTime = targetTime,
                            createdAt = createdAt,
                            isRecurring = isRecurring,
                            recurrenceType = recurrenceType,
                            dailyInterval = 1,
                            weeklyDays = emptySet(),
                            monthlyType = monthlyType,
                            monthlyDates = monthlyDates,
                            monthlyWeek = monthlyWeek,
                            monthlyDayOfWeek = monthlyDayOfWeek,
                            annuallyType = annuallyType,
                            annuallyMonth = annuallyMonth,
                            annuallyDates = annuallyDates,
                            annuallyWeek = annuallyWeek,
                            annuallyDayOfWeek = annuallyDayOfWeek,
                            occurrenceCount = occurrenceCount,
                            editingId = editingTask?.id,
                            priority = priority,
                            deadlineDateTime = deadlineDateTime,
                            link = link.takeIf { it.isNotBlank() },
                            attachmentUri = attachmentUri.takeIf { it.isNotBlank() }
                        )
                    )
                    viewModel.setEditingTask(null)
                    viewModel.setCreatingChronometer(false)
                },
                modifier = Modifier.size(48.dp)
            ) {
                Icon(Icons.Default.Check, contentDescription = "Save", tint = MaterialTheme.colorScheme.primary)
            }
        }
        
        HorizontalDivider(color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f))
        
        LazyColumn(
            modifier = Modifier
                .weight(1f)
                .fillMaxWidth()
                .padding(horizontal = 16.dp),
            contentPadding = PaddingValues(vertical = 16.dp),
            verticalArrangement = Arrangement.spacedBy(24.dp)
        ) {
            // Basic Inputs
            item {
                Text("TIMER LABEL / TASK NAME", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f), fontSize = 12.sp, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(8.dp))
                OutlinedTextField(
                    value = name,
                    onValueChange = { if (it.length <= 30) name = it },
                    placeholder = { Text("e.g., Marketing Deck, Shift Target", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.4f)) },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = MaterialTheme.colorScheme.primary,
                        unfocusedBorderColor = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.2f),
                    ),
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(imeAction = androidx.compose.ui.text.input.ImeAction.Next),
                    supportingText = { Text("${name.length}/30") }
                )
            }
            
            item {
                Text("DESCRIPTION (OPTIONAL)", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f), fontSize = 12.sp, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(8.dp))
                OutlinedTextField(
                    value = description,
                    onValueChange = { if (it.length <= 200) description = it },
                    placeholder = { Text("Add some context or details here...", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.4f)) },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = MaterialTheme.colorScheme.primary,
                        unfocusedBorderColor = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.2f),
                    ),
                    maxLines = 4,
                    minLines = 3,
                    keyboardOptions = KeyboardOptions(imeAction = androidx.compose.ui.text.input.ImeAction.Default),
                    trailingIcon = {
                        Column {
                            IconButton(
                                onClick = { showLinkDialog = true }
                            ) {
                                Icon(Icons.Default.AddLink, contentDescription = "Add Link")
                            }
                            IconButton(
                                onClick = { filePickerLauncher.launch(arrayOf("*/*")) }
                            ) {
                                Icon(androidx.compose.material.icons.Icons.Default.AttachFile, contentDescription = "Attachment")
                            }
                            IconButton(onClick = { keyboardController?.hide() }) {
                                Icon(Icons.Default.Check, contentDescription = "Done")
                            }
                        }
                    },
                    supportingText = { Text("${description.length}/200") }
                )
                
                if (link.isNotEmpty() || attachmentUri.isNotEmpty()) {
                    Spacer(Modifier.height(8.dp))
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        if (link.isNotEmpty()) {
                            val uriHandler = androidx.compose.ui.platform.LocalUriHandler.current
                            Row(
                                modifier = Modifier
                                    .clip(RoundedCornerShape(8.dp))
                                    .background(MaterialTheme.colorScheme.primaryContainer)
                                    .clickable { 
                                        try { uriHandler.openUri(link) } catch (e:Exception) {} 
                                    }
                                    .padding(8.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Icon(Icons.Default.AddLink, contentDescription = null, tint = MaterialTheme.colorScheme.onPrimaryContainer, modifier = Modifier.size(16.dp))
                                Spacer(Modifier.width(4.dp))
                                Text("Link attached", color = MaterialTheme.colorScheme.onPrimaryContainer, fontSize = 12.sp, textDecoration = androidx.compose.ui.text.style.TextDecoration.Underline)
                            }
                        }
                        if (attachmentUri.isNotEmpty()) {
                            Row(
                                modifier = Modifier
                                    .clip(RoundedCornerShape(8.dp))
                                    .background(MaterialTheme.colorScheme.tertiaryContainer)
                                    .clickable { 
                                        try {
                                            val intent = android.content.Intent(android.content.Intent.ACTION_VIEW)
                                            intent.setData(android.net.Uri.parse(attachmentUri))
                                            intent.addFlags(android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION)
                                            context.startActivity(intent)
                                        } catch (e: Exception) {
                                            android.widget.Toast.makeText(context, "Cannot open file", android.widget.Toast.LENGTH_SHORT).show()
                                        }
                                    }
                                    .padding(8.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Icon(androidx.compose.material.icons.Icons.Default.AttachFile, contentDescription = null, tint = MaterialTheme.colorScheme.onTertiaryContainer, modifier = Modifier.size(16.dp))
                                Spacer(Modifier.width(4.dp))
                                Text("File attached", color = MaterialTheme.colorScheme.onTertiaryContainer, fontSize = 12.sp)
                            }
                        }
                    }
                }
            }
            
            // Tags
            item {
                Text("TAGS", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f), fontSize = 12.sp, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(8.dp))
                val chunkedTags = if (availableTags.size > 3) {
                    val half = (availableTags.size + 1) / 2
                    listOf(availableTags.take(half), availableTags.drop(half))
                } else {
                    listOf(availableTags)
                }

                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .horizontalScroll(rememberScrollState())
                ) {
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        chunkedTags.forEach { rowTags ->
                            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                rowTags.forEach { label ->
                                    val isSelected = selectedTags.contains(label)
                                    val tagColor = getLabelColor(label, uiState.coloredLabelsEnabled)
                                    FilterChip(
                                        selected = isSelected,
                                        onClick = { 
                                            selectedTags = if (isSelected) selectedTags - label else selectedTags + label 
                                        },
                                        label = { Text(getLabelName(label), fontSize = 16.sp, fontWeight = FontWeight.Bold) },
                                        modifier = Modifier.height(36.dp),
                                        colors = FilterChipDefaults.filterChipColors(
                                            selectedContainerColor = if (tagColor != Color.Transparent) tagColor.copy(alpha = 0.3f) else MaterialTheme.colorScheme.primaryContainer,
                                            selectedLabelColor = if (tagColor != Color.Transparent) tagColor else MaterialTheme.colorScheme.onPrimaryContainer,
                                            labelColor = if (tagColor != Color.Transparent) tagColor else MaterialTheme.colorScheme.onSurfaceVariant
                                        ),
                                        border = FilterChipDefaults.filterChipBorder(
                                            enabled = true,
                                            selected = isSelected,
                                            borderColor = if (tagColor != Color.Transparent) tagColor.copy(alpha = 0.5f) else MaterialTheme.colorScheme.outline
                                        )
                                    )
                                }
                            }
                        }
                    }
                }
            }
            
            // Start Date
            item {
                Text("START TIME", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f), fontSize = 12.sp, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(8.dp))
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(12.dp))
                        .background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                        .clickable { showCreatedPicker = true }
                        .padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.DateRange, contentDescription = null, tint = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f), modifier = Modifier.size(16.dp))
                        Spacer(Modifier.width(8.dp))
                        Text(formatDateTime(createdAt), color = MaterialTheme.colorScheme.onSurface)
                    }
                }
                
                Spacer(Modifier.height(8.dp))
                // Quick Modifiers for Start
                Row(modifier = Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                    val modifyStart = { ms: Long -> createdAt += ms }
                    val chipModifier = Modifier.width(42.dp).height(36.dp)
                    Button(onClick = { modifyStart(-30L * 86400000L) }, modifier = chipModifier, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f), contentColor = MaterialTheme.colorScheme.onSurface), contentPadding = PaddingValues(0.dp)) { Text("-1M", fontSize = 12.sp) }
                    Button(onClick = { modifyStart(-7L * 86400000L) }, modifier = chipModifier, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f), contentColor = MaterialTheme.colorScheme.onSurface), contentPadding = PaddingValues(0.dp)) { Text("-1w", fontSize = 12.sp) }
                    Button(onClick = { modifyStart(-86400000L) }, modifier = chipModifier, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f), contentColor = MaterialTheme.colorScheme.onSurface), contentPadding = PaddingValues(0.dp)) { Text("-1d", fontSize = 12.sp) }
                    Button(onClick = { modifyStart(-15L * 60000L) }, modifier = chipModifier, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f), contentColor = MaterialTheme.colorScheme.onSurface), contentPadding = PaddingValues(0.dp)) { Text("-15m", fontSize = 12.sp) }
                    Button(onClick = { modifyStart(15L * 60000L) }, modifier = chipModifier, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f), contentColor = MaterialTheme.colorScheme.onSurface), contentPadding = PaddingValues(0.dp)) { Text("+15m", fontSize = 12.sp) }
                    Button(onClick = { modifyStart(86400000L) }, modifier = chipModifier, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f), contentColor = MaterialTheme.colorScheme.onSurface), contentPadding = PaddingValues(0.dp)) { Text("+1d", fontSize = 12.sp) }
                    Button(onClick = { modifyStart(7L * 86400000L) }, modifier = chipModifier, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f), contentColor = MaterialTheme.colorScheme.onSurface), contentPadding = PaddingValues(0.dp)) { Text("+1w", fontSize = 12.sp) }
                    Button(onClick = { modifyStart(30L * 86400000L) }, modifier = chipModifier, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f), contentColor = MaterialTheme.colorScheme.onSurface), contentPadding = PaddingValues(0.dp)) { Text("+1M", fontSize = 12.sp) }
                }
            }
            
            // Target Date
            item {
                Text("TARGET DEADLINE", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f), fontSize = 12.sp, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(8.dp))
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(12.dp))
                        .background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                        .clickable { showTargetPicker = true }
                        .padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.DateRange, contentDescription = null, tint = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f), modifier = Modifier.size(16.dp))
                        Spacer(Modifier.width(8.dp))
                        Text(formatDateTime(targetTime), color = MaterialTheme.colorScheme.onSurface)
                    }
                }
                
                Spacer(Modifier.height(8.dp))
                // Quick Modifiers for Target
                Row(modifier = Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                    val modifyTarget = { ms: Long -> targetTime += ms }
                    val chipModifier = Modifier.width(42.dp).height(36.dp)
                    Button(onClick = { modifyTarget(-30L * 86400000L) }, modifier = chipModifier, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f), contentColor = MaterialTheme.colorScheme.onSurface), contentPadding = PaddingValues(0.dp)) { Text("-1M", fontSize = 12.sp) }
                    Button(onClick = { modifyTarget(-7L * 86400000L) }, modifier = chipModifier, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f), contentColor = MaterialTheme.colorScheme.onSurface), contentPadding = PaddingValues(0.dp)) { Text("-1w", fontSize = 12.sp) }
                    Button(onClick = { modifyTarget(-86400000L) }, modifier = chipModifier, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f), contentColor = MaterialTheme.colorScheme.onSurface), contentPadding = PaddingValues(0.dp)) { Text("-1d", fontSize = 12.sp) }
                    Button(onClick = { modifyTarget(-15L * 60000L) }, modifier = chipModifier, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f), contentColor = MaterialTheme.colorScheme.onSurface), contentPadding = PaddingValues(0.dp)) { Text("-15m", fontSize = 12.sp) }
                    Button(onClick = { modifyTarget(15L * 60000L) }, modifier = chipModifier, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f), contentColor = MaterialTheme.colorScheme.onSurface), contentPadding = PaddingValues(0.dp)) { Text("+15m", fontSize = 12.sp) }
                    Button(onClick = { modifyTarget(86400000L) }, modifier = chipModifier, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f), contentColor = MaterialTheme.colorScheme.onSurface), contentPadding = PaddingValues(0.dp)) { Text("+1d", fontSize = 12.sp) }
                    Button(onClick = { modifyTarget(7L * 86400000L) }, modifier = chipModifier, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f), contentColor = MaterialTheme.colorScheme.onSurface), contentPadding = PaddingValues(0.dp)) { Text("+1w", fontSize = 12.sp) }
                    Button(onClick = { modifyTarget(30L * 86400000L) }, modifier = chipModifier, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f), contentColor = MaterialTheme.colorScheme.onSurface), contentPadding = PaddingValues(0.dp)) { Text("+1M", fontSize = 12.sp) }
                }
            }
            
            // Priority and Deadline
            item {
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    val context = androidx.compose.ui.platform.LocalContext.current
                    Box(modifier = Modifier.weight(1f)) {
                        val priorityColor = when (priority) {
                            "High" -> androidx.compose.ui.graphics.Color(0xFFE57373)
                            "Normal" -> androidx.compose.material3.MaterialTheme.colorScheme.onSurfaceVariant
                            "Low" -> androidx.compose.ui.graphics.Color(0xFF81C784)
                            else -> androidx.compose.material3.MaterialTheme.colorScheme.onSurfaceVariant
                        }
                        androidx.compose.material3.OutlinedButton(
                            onClick = { showPriorityMenu = true },
                            modifier = Modifier.fillMaxWidth().height(48.dp),
                            shape = androidx.compose.foundation.shape.RoundedCornerShape(12.dp),
                            colors = androidx.compose.material3.ButtonDefaults.outlinedButtonColors(contentColor = priorityColor),
                            border = androidx.compose.foundation.BorderStroke(1.dp, priorityColor.copy(alpha = 0.5f))
                        ) {
                            androidx.compose.material3.Icon(Icons.Default.Info, contentDescription = "Priority", modifier = Modifier.size(16.dp))
                            Spacer(Modifier.width(8.dp))
                            Text(priority)
                        }
                        DropdownMenu(
                            expanded = showPriorityMenu,
                            onDismissRequest = { showPriorityMenu = false }
                        ) {
                            DropdownMenuItem(
                                text = { Text("High") },
                                onClick = { priority = "High"; showPriorityMenu = false }
                            )
                            DropdownMenuItem(
                                text = { Text("Normal") },
                                onClick = { priority = "Normal"; showPriorityMenu = false }
                            )
                            DropdownMenuItem(
                                text = { Text("Low") },
                                onClick = { priority = "Low"; showPriorityMenu = false }
                            )
                        }
                    }
                    Box(modifier = Modifier.weight(1f)) {
                        val deadlineText = if (deadlineDateTime != null) {
                            val diff = targetTime - deadlineDateTime!!
                            if (diff == 30 * 60 * 1000L) "30m before"
                            else if (diff == 60 * 60 * 1000L) "1h before"
                            else "Custom"
                        } else "Deadline"
                        val deadlineColor = if (deadlineDateTime != null) MaterialTheme.colorScheme.primary else androidx.compose.material3.MaterialTheme.colorScheme.onSurfaceVariant
                        androidx.compose.material3.OutlinedButton(
                            onClick = { showDeadlineMenu = true },
                            modifier = Modifier.fillMaxWidth().height(48.dp),
                            shape = androidx.compose.foundation.shape.RoundedCornerShape(12.dp),
                            colors = androidx.compose.material3.ButtonDefaults.outlinedButtonColors(contentColor = deadlineColor),
                            border = androidx.compose.foundation.BorderStroke(1.dp, deadlineColor.copy(alpha = 0.5f))
                        ) {
                            androidx.compose.material3.Icon(Icons.Default.Notifications, contentDescription = "Deadline", modifier = Modifier.size(16.dp))
                            Spacer(Modifier.width(8.dp))
                            Text(deadlineText)
                        }
                        DropdownMenu(
                            expanded = showDeadlineMenu,
                            onDismissRequest = { showDeadlineMenu = false }
                        ) {
                            DropdownMenuItem(
                                text = { Text("30 mins before") },
                                onClick = { 
                                    val newDeadline = targetTime - (30 * 60 * 1000L)
                                    if (newDeadline >= createdAt) {
                                        deadlineDateTime = newDeadline
                                    } else {
                                        android.widget.Toast.makeText(context, "Cannot set before start time", android.widget.Toast.LENGTH_SHORT).show()
                                    }
                                    showDeadlineMenu = false 
                                }
                            )
                            DropdownMenuItem(
                                text = { Text("1 hour before") },
                                onClick = { 
                                    val newDeadline = targetTime - (60 * 60 * 1000L)
                                    if (newDeadline >= createdAt) {
                                        deadlineDateTime = newDeadline
                                    } else {
                                        android.widget.Toast.makeText(context, "Cannot set before start time", android.widget.Toast.LENGTH_SHORT).show()
                                    }
                                    showDeadlineMenu = false 
                                }
                            )
                            DropdownMenuItem(
                                text = { Text("Custom...") },
                                onClick = { 
                                    showDeadlineMenu = false 
                                    showCustomDeadlinePicker = true
                                }
                            )
                            DropdownMenuItem(
                                text = { Text("Clear") },
                                onClick = { 
                                    deadlineDateTime = null
                                    showDeadlineMenu = false 
                                }
                            )
                        }
                    }
                }
            }
            item { Spacer(Modifier.height(8.dp)) }
            
            item {
                Row(
                    modifier = Modifier.fillMaxWidth().padding(top = 16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("Recurring Deadline", fontSize = 18.sp, fontWeight = FontWeight.Bold)
                    Switch(checked = isRecurring, onCheckedChange = { isRecurring = it })
                }
            }
            
            if (isRecurring) {
                item {
                    Text(text = dynamicString, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Medium)
                }
                
                item {
                    // Recurrence Count
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text("Number of occurrences: ", fontSize = 16.sp, modifier = Modifier.weight(1f))
                        
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                            Box(
                                modifier = Modifier
                                    .size(64.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.surfaceVariant)
                                    .pointerInput(Unit) {
                                        detectTapGestures(
                                            onPress = {
                                                minusHolding = true
                                                tryAwaitRelease()
                                                minusHolding = false
                                            }
                                        )
                                    },
                                contentAlignment = Alignment.Center
                            ) {
                                Text("-", fontSize = 36.sp, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                            }
                            
                            Text(
                                text = if (occurrenceCount <= 0) "∞" else "$occurrenceCount",
                                fontWeight = FontWeight.Bold,
                                fontSize = 24.sp,
                                modifier = Modifier.widthIn(min = 40.dp),
                                textAlign = androidx.compose.ui.text.style.TextAlign.Center
                            )
                            
                            Box(
                                modifier = Modifier
                                    .size(64.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.surfaceVariant)
                                    .pointerInput(Unit) {
                                        detectTapGestures(
                                            onPress = {
                                                plusHolding = true
                                                tryAwaitRelease()
                                                plusHolding = false
                                            }
                                        )
                                    },
                                contentAlignment = Alignment.Center
                            ) {
                                Text("+", fontSize = 36.sp, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
                
                item {
                    ScrollableTabRow(
                        selectedTabIndex = when (recurrenceType) {
                            RecurrenceType.MONTHLY -> 0
                            RecurrenceType.ANNUALLY -> 1
                            else -> 0
                        },
                        edgePadding = 0.dp
                    ) {
                        Tab(selected = recurrenceType == RecurrenceType.MONTHLY, onClick = { recurrenceType = RecurrenceType.MONTHLY }) { Text("Monthly", modifier = Modifier.padding(16.dp)) }
                        Tab(selected = recurrenceType == RecurrenceType.ANNUALLY, onClick = { recurrenceType = RecurrenceType.ANNUALLY }) { Text("Annually", modifier = Modifier.padding(16.dp)) }
                    }
                }
                
                item {
when (recurrenceType) {
                    RecurrenceType.MONTHLY -> {
                        var expandedType by remember { mutableStateOf(false) }
                        ExposedDropdownMenuBox(expanded = expandedType, onExpandedChange = { expandedType = it }) {
                            OutlinedTextField(
                                value = when(monthlyType) {
                                    MonthlyType.DATES -> "Select Dates"
                                    MonthlyType.LAST_DAY -> "Last day of the month"
                                    MonthlyType.DAY_OF_WEEK -> "Day of the week"
                                },
                                onValueChange = {},
                                readOnly = true,
                                trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expandedType) },
                                modifier = Modifier.menuAnchor().fillMaxWidth()
                            )
                            ExposedDropdownMenu(expanded = expandedType, onDismissRequest = { expandedType = false }) {
                                DropdownMenuItem(text = { Text("Select Dates") }, onClick = { monthlyType = MonthlyType.DATES; expandedType = false })
                                DropdownMenuItem(text = { Text("Last day of the month") }, onClick = { monthlyType = MonthlyType.LAST_DAY; expandedType = false })
                                DropdownMenuItem(text = { Text("Day of the week") }, onClick = { monthlyType = MonthlyType.DAY_OF_WEEK; expandedType = false })
                            }
                        }
                        
                        if (monthlyType == MonthlyType.DATES) {
                            // Quick grid of 1-31
                            var datesInput by remember { mutableStateOf(monthlyDates.joinToString(",")) }
                            OutlinedTextField(
                                value = datesInput,
                                onValueChange = { 
                                    datesInput = it
                                    val parsed = parseDateString(it)
                                    monthlyDates = parsed

                                },
                                label = { Text("Dates (e.g., 1-5, 10, 15-20)") },
                                modifier = Modifier.fillMaxWidth()
                            )
                        } else if (monthlyType == MonthlyType.DAY_OF_WEEK) {
                            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                var expandedWeek by remember { mutableStateOf(false) }
                                ExposedDropdownMenuBox(expanded = expandedWeek, onExpandedChange = { expandedWeek = it }, modifier = Modifier.weight(1f)) {
                                    OutlinedTextField(
                                        value = getWeekName(monthlyWeek),
                                        onValueChange = {}, readOnly = true, trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expandedWeek) }, modifier = Modifier.menuAnchor().fillMaxWidth()
                                    )
                                    ExposedDropdownMenu(expanded = expandedWeek, onDismissRequest = { expandedWeek = false }) {
                                        (1..5).forEach { w ->
                                            DropdownMenuItem(text = { Text(getWeekName(w)) }, onClick = { monthlyWeek = w; expandedWeek = false })
                                        }
                                    }
                                }
                                var expandedDay by remember { mutableStateOf(false) }
                                ExposedDropdownMenuBox(expanded = expandedDay, onExpandedChange = { expandedDay = it }, modifier = Modifier.weight(1f)) {
                                    OutlinedTextField(
                                        value = getDayOfWeekName(monthlyDayOfWeek),
                                        onValueChange = {}, readOnly = true, trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expandedDay) }, modifier = Modifier.menuAnchor().fillMaxWidth()
                                    )
                                    ExposedDropdownMenu(expanded = expandedDay, onDismissRequest = { expandedDay = false }) {
                                        (Calendar.SUNDAY..Calendar.SATURDAY).forEach { d ->
                                            DropdownMenuItem(text = { Text(getDayOfWeekName(d)) }, onClick = { monthlyDayOfWeek = d; expandedDay = false })
                                        }
                                    }
                                }
                            }
                        }
                    }
                    RecurrenceType.ANNUALLY -> {
                        var expandedMonth by remember { mutableStateOf(false) }
                        ExposedDropdownMenuBox(expanded = expandedMonth, onExpandedChange = { expandedMonth = it }) {
                            OutlinedTextField(
                                value = getMonthName(annuallyMonth),
                                onValueChange = {}, readOnly = true, trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expandedMonth) }, modifier = Modifier.menuAnchor().fillMaxWidth()
                            )
                            ExposedDropdownMenu(expanded = expandedMonth, onDismissRequest = { expandedMonth = false }) {
                                (Calendar.JANUARY..Calendar.DECEMBER).forEach { m ->
                                    DropdownMenuItem(text = { Text(getMonthName(m)) }, onClick = { annuallyMonth = m; expandedMonth = false })
                                }
                            }
                        }
                        
                        var expandedType by remember { mutableStateOf(false) }
                        ExposedDropdownMenuBox(expanded = expandedType, onExpandedChange = { expandedType = it }) {
                            OutlinedTextField(
                                value = when(annuallyType) {
                                    AnnuallyType.DATES -> "Select Dates"
                                    AnnuallyType.END_OF_YEAR -> "End of year"
                                    AnnuallyType.DAY_OF_WEEK -> "Day of the week"
                                },
                                onValueChange = {},
                                readOnly = true,
                                trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expandedType) },
                                modifier = Modifier.menuAnchor().fillMaxWidth()
                            )
                            ExposedDropdownMenu(expanded = expandedType, onDismissRequest = { expandedType = false }) {
                                DropdownMenuItem(text = { Text("Select Dates") }, onClick = { annuallyType = AnnuallyType.DATES; expandedType = false })
                                DropdownMenuItem(text = { Text("End of year") }, onClick = { annuallyType = AnnuallyType.END_OF_YEAR; expandedType = false })
                                DropdownMenuItem(text = { Text("Day of the week") }, onClick = { annuallyType = AnnuallyType.DAY_OF_WEEK; expandedType = false })
                            }
                        }
                        
                        if (annuallyType == AnnuallyType.DATES) {
                            var datesInput by remember { mutableStateOf(annuallyDates.joinToString(",")) }
                            OutlinedTextField(
                                value = datesInput,
                                onValueChange = { 
                                    datesInput = it
                                    val parsed = parseDateString(it)
                                    annuallyDates = parsed
                                },
                                label = { Text("Dates (e.g., 1-5, 10, 15-20)") },
                                modifier = Modifier.fillMaxWidth()
                            )
                        } else if (annuallyType == AnnuallyType.DAY_OF_WEEK) {
                            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                var expandedWeek by remember { mutableStateOf(false) }
                                ExposedDropdownMenuBox(expanded = expandedWeek, onExpandedChange = { expandedWeek = it }, modifier = Modifier.weight(1f)) {
                                    OutlinedTextField(
                                        value = getWeekName(annuallyWeek),
                                        onValueChange = {}, readOnly = true, trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expandedWeek) }, modifier = Modifier.menuAnchor().fillMaxWidth()
                                    )
                                    ExposedDropdownMenu(expanded = expandedWeek, onDismissRequest = { expandedWeek = false }) {
                                        (1..5).forEach { w ->
                                            DropdownMenuItem(text = { Text(getWeekName(w)) }, onClick = { annuallyWeek = w; expandedWeek = false })
                                        }
                                    }
                                }
                                var expandedDay by remember { mutableStateOf(false) }
                                ExposedDropdownMenuBox(expanded = expandedDay, onExpandedChange = { expandedDay = it }, modifier = Modifier.weight(1f)) {
                                    OutlinedTextField(
                                        value = getDayOfWeekName(annuallyDayOfWeek),
                                        onValueChange = {}, readOnly = true, trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expandedDay) }, modifier = Modifier.menuAnchor().fillMaxWidth()
                                    )
                                    ExposedDropdownMenu(expanded = expandedDay, onDismissRequest = { expandedDay = false }) {
                                        (Calendar.SUNDAY..Calendar.SATURDAY).forEach { d ->
                                            DropdownMenuItem(text = { Text(getDayOfWeekName(d)) }, onClick = { annuallyDayOfWeek = d; expandedDay = false })
                                        }
                                    }
                                }
                            }
                        }
                    }
                    else -> {}
                }
            }
            }
        }
    }
}
