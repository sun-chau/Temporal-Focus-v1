import os

new_code = """package com.example.ui.screens

import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.GridItemSpan
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.border
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.KeyboardArrowDown
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.RectangleShape
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.launch
import com.example.data.*
import com.example.viewmodel.TrackerViewModel
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.UUID

@OptIn(ExperimentalFoundationApi::class, ExperimentalMaterial3Api::class)
@Composable
fun BurnRateTrackerUI(
    entity: TrackerEntity,
    payload: BurnRatePayload,
    viewModel: TrackerViewModel
) {
    var inputStr by remember { mutableStateOf("") }
    var selectedTag by remember { mutableStateOf("GENERAL") }
    var showLimitDialog by remember { mutableStateOf(false) }
    var showAddTagDialog by remember { mutableStateOf(false) }
    var tagToDelete by remember { mutableStateOf<String?>(null) }
    
    var transactionToEdit by remember { mutableStateOf<Transaction?>(null) }
    var isArchiveMode by remember { mutableStateOf(false) }
    
    val pastMonths = remember { (0..11).map { java.time.YearMonth.now().minusMonths(it.toLong()) } }
    var selectedArchiveMonth by remember { mutableStateOf(pastMonths[0]) }
    var archiveTagFilter by remember { mutableStateOf("ALL") }

    val listState = rememberLazyListState()
    val coroutineScope = rememberCoroutineScope()
    val showScrollToLatest by remember { derivedStateOf { listState.firstVisibleItemIndex > 2 } }

    val tags = listOf("GENERAL", "FOOD", "TRANSPORT") + payload.customTags.toList()
    if (selectedTag !in tags) {
        selectedTag = "GENERAL"
    }

    val activeMonthTx = if (!isArchiveMode) {
        viewModel.getActiveCycleTransactions(payload).sortedByDescending { it.timestampEpoch }
    } else {
        val mStart = selectedArchiveMonth.atDay(payload.cycleStartDay.coerceIn(1, 28)).atStartOfDay(java.time.ZoneId.systemDefault()).toInstant().toEpochMilli()
        val mEnd = selectedArchiveMonth.plusMonths(1).atDay(payload.cycleStartDay.coerceIn(1, 28)).atStartOfDay(java.time.ZoneId.systemDefault()).toInstant().toEpochMilli()
        payload.transactions.filter {
            it.timestampEpoch in mStart until mEnd && (archiveTagFilter == "ALL" || it.tag == archiveTagFilter)
        }.sortedByDescending { it.timestampEpoch }
    }
    
    val activeSum = activeMonthTx.sumOf { it.amount }

    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        
        // SEGMENTED TOGGLE
        Row(
            modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp),
            horizontalArrangement = Arrangement.Center
        ) {
            FilterChip(
                selected = !isArchiveMode,
                onClick = { isArchiveMode = false },
                label = { Text("[ ACTIVE CYCLE ]", fontWeight = FontWeight.Bold) }
            )
            Spacer(Modifier.width(8.dp))
            FilterChip(
                selected = isArchiveMode,
                onClick = { isArchiveMode = true },
                label = { Text("[ ARCHIVE ]", fontWeight = FontWeight.Bold) }
            )
        }

        if (!isArchiveMode) {
            // Top Fraction
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .border(2.dp, MaterialTheme.colorScheme.outline, RectangleShape)
                    .clickable { showLimitDialog = true }
                    .padding(16.dp),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = "₹%.2f / ₹%.2f".format(activeSum, payload.monthlyLimit),
                    modifier = Modifier.horizontalScroll(rememberScrollState()),
                    style = MaterialTheme.typography.headlineMedium,
                    fontWeight = FontWeight.Bold,
                    fontFamily = FontFamily.Monospace,
                    color = if (payload.monthlyLimit > 0.0 && activeSum > payload.monthlyLimit) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.onSurface,
                    maxLines = 1
                )
            }
            Spacer(modifier = Modifier.height(16.dp))

            // Input Display
            Text(
                text = if (inputStr.isEmpty()) "₹0.00" else "₹$inputStr",
                style = MaterialTheme.typography.displayMedium,
                fontFamily = FontFamily.Monospace,
                color = MaterialTheme.colorScheme.primary,
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(modifier = Modifier.height(8.dp))

            // Tag Bar
            LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                items(tags) { tag ->
                    FilterChip(
                        selected = selectedTag == tag,
                        onClick = { selectedTag = tag },
                        label = { Text(tag) },
                        modifier = Modifier.combinedClickable(
                            onClick = { selectedTag = tag },
                            onLongClick = {
                                if (tag !in listOf("GENERAL", "FOOD", "TRANSPORT")) {
                                    tagToDelete = tag
                                }
                            }
                        )
                    )
                }
                item {
                    AssistChip(
                        onClick = { showAddTagDialog = true },
                        label = { Text("+ TAG") }
                    )
                }
            }
        } else {
            // ARCHIVE UI
            val monthFormat = java.time.format.DateTimeFormatter.ofPattern("MMM yyyy")
            LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                items(pastMonths) { m ->
                    FilterChip(
                        selected = selectedArchiveMonth == m,
                        onClick = { selectedArchiveMonth = m },
                        label = { Text(m.format(monthFormat).uppercase()) }
                    )
                }
            }
            val archiveTags = listOf("ALL") + tags
            LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.padding(top = 8.dp)) {
                items(archiveTags) { t ->
                    FilterChip(
                        selected = archiveTagFilter == t,
                        onClick = { archiveTagFilter = t },
                        label = { Text(t) }
                    )
                }
            }
            Spacer(modifier = Modifier.height(16.dp))
            Text(
                text = "₹%.2f SPENT ON %s IN %s".format(activeSum, archiveTagFilter, selectedArchiveMonth.format(monthFormat).uppercase()),
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.primary
            )
        }

        Spacer(modifier = Modifier.height(8.dp))
        HorizontalDivider()
        Spacer(modifier = Modifier.height(8.dp))

        // Ledger
        val dateFormat = SimpleDateFormat("dd MMM, HH:mm", Locale.getDefault())
        Box(modifier = Modifier.weight(1f)) {
            LazyColumn(
                state = listState,
                modifier = Modifier.fillMaxSize(),
                reverseLayout = !isArchiveMode // only reverse in active cycle to pin to bottom
            ) {
                items(activeMonthTx, key = { it.id }) { tx ->
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .combinedClickable(
                                onClick = {},
                                onLongClick = { transactionToEdit = tx }
                            )
                            .padding(vertical = 8.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column(modifier = Modifier.weight(1f)) {
                            Text(
                                text = "₹%.2f".format(tx.amount),
                                style = MaterialTheme.typography.titleMedium,
                                fontFamily = FontFamily.Monospace,
                                fontWeight = FontWeight.Bold,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                            Text(
                                text = dateFormat.format(Date(tx.timestampEpoch)),
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                        Spacer(modifier = Modifier.width(8.dp))
                        Surface(
                            shape = MaterialTheme.shapes.small,
                            color = MaterialTheme.colorScheme.secondaryContainer
                        ) {
                            Text(
                                text = tx.tag,
                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                                style = MaterialTheme.typography.labelMedium
                            )
                        }
                    }
                }
            }
            if (!isArchiveMode) {
                ScrollToLatestButton(
                    visible = showScrollToLatest,
                    onClick = { coroutineScope.launch { listState.animateScrollToItem(0) } },
                    modifier = Modifier
                        .align(Alignment.BottomEnd)
                        .padding(16.dp)
                )
            }
        }

        if (!isArchiveMode) {
            Spacer(modifier = Modifier.height(8.dp))
            // Numpad
            val keys = listOf("1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "0", "DEL", "DEDUCT")
            LazyVerticalGrid(
                columns = GridCells.Fixed(3),
                modifier = Modifier.fillMaxWidth()
            ) {
                items(keys, span = { key ->
                    if (key == "DEDUCT") GridItemSpan(3) else GridItemSpan(1)
                }) { key ->
                    Box(
                        modifier = Modifier
                            .aspectRatio(if (key == "DEDUCT") 6f else 2f)
                            .padding(4.dp)
                            .background(
                                color = if (key == "DEDUCT") MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                                shape = MaterialTheme.shapes.medium
                            )
                            .clickable {
                                if (key == "DEDUCT") {
                                    val amt = inputStr.toDoubleOrNull() ?: 0.0
                                    if (amt > 0.0) {
                                        val newTx = Transaction(
                                            id = UUID.randomUUID().toString(),
                                            amount = amt,
                                            timestampEpoch = System.currentTimeMillis(),
                                            tag = selectedTag
                                        )
                                        viewModel.updateBurnRatePayload(
                                            entity,
                                            payload.copy(transactions = listOf(newTx) + payload.transactions)
                                        )
                                        inputStr = ""
                                    } else {
                                        inputStr = ""
                                    }
                                } else if (key == "DEL") {
                                    if (inputStr.isNotEmpty()) inputStr = inputStr.dropLast(1)
                                } else if (key == ".") {
                                    if (!inputStr.contains(".")) inputStr += "."
                                } else {
                                    if (inputStr.contains(".") && inputStr.substringAfter(".", "").length >= 2) {
                                        // limit decimals
                                    } else {
                                        inputStr += key
                                    }
                                }
                            },
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = key,
                            color = if (key == "DEDUCT") MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurface,
                            fontSize = 20.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }
            }
        }
    }

    if (showLimitDialog) {
        var limitInput by remember { mutableStateOf(payload.monthlyLimit.toString()) }
        var cycleInput by remember { mutableStateOf(payload.cycleStartDay.toString()) }
        AlertDialog(
            onDismissRequest = { showLimitDialog = false },
            title = { Text("Budget Settings") },
            text = {
                Column {
                    OutlinedTextField(
                        value = limitInput,
                        onValueChange = { limitInput = it },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        singleLine = true,
                        modifier = Modifier.fillMaxWidth(),
                        label = { Text("Monthly Limit") }
                    )
                    Spacer(Modifier.height(8.dp))
                    OutlinedTextField(
                        value = cycleInput,
                        onValueChange = { cycleInput = it },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        singleLine = true,
                        modifier = Modifier.fillMaxWidth(),
                        label = { Text("Cycle Start Day (1-28)") }
                    )
                }
            },
            confirmButton = {
                TextButton(
                    onClick = {
                        val limit = limitInput.toDoubleOrNull() ?: payload.monthlyLimit
                        val cycle = cycleInput.toIntOrNull()?.coerceIn(1, 28) ?: payload.cycleStartDay
                        viewModel.updateBurnRatePayload(entity, payload.copy(monthlyLimit = limit, cycleStartDay = cycle))
                        showLimitDialog = false
                    }
                ) { Text("SAVE CHANGES", fontWeight = FontWeight.Bold) }
            },
            dismissButton = {
                TextButton(onClick = { showLimitDialog = false }) { Text("CANCEL") }
            }
        )
    }

    if (showAddTagDialog) {
        var newTagInput by remember { mutableStateOf("") }
        AlertDialog(
            onDismissRequest = { showAddTagDialog = false },
            title = { Text("Add Custom Tag") },
            text = {
                OutlinedTextField(
                    value = newTagInput,
                    onValueChange = { newTagInput = it.uppercase() },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth(),
                    label = { Text("Tag Name") }
                )
            },
            confirmButton = {
                val hasChanges = newTagInput.isNotBlank()
                TextButton(
                    onClick = {
                        if (newTagInput.isNotBlank()) {
                            viewModel.addBurnRateTag(entity, newTagInput)
                        }
                        showAddTagDialog = false
                    },
                    enabled = hasChanges
                ) { Text("SAVE CHANGES", fontWeight = FontWeight.Bold) }
            },
            dismissButton = {
                TextButton(onClick = { showAddTagDialog = false }) { Text("CANCEL") }
            }
        )
    }

    if (tagToDelete != null) {
        val tag = tagToDelete!!
        AlertDialog(
            onDismissRequest = { tagToDelete = null },
            title = { Text("Delete Tag") },
            text = { Text("Are you sure you want to delete the tag '[ $tag ]'? This will not delete past transactions using this tag.") },
            confirmButton = {
                TextButton(
                    onClick = {
                        viewModel.deleteBurnRateTag(entity, tag)
                        if (selectedTag == tag) {
                            selectedTag = "GENERAL"
                        }
                        tagToDelete = null
                    }
                ) { Text("DELETE", color = MaterialTheme.colorScheme.error, fontWeight = FontWeight.Bold) }
            },
            dismissButton = {
                TextButton(onClick = { tagToDelete = null }) { Text("CANCEL") }
            }
        )
    }

    if (transactionToEdit != null) {
        TransactionEditSheet(
            tx = transactionToEdit!!,
            tags = tags,
            onDismiss = { transactionToEdit = null },
            onSave = { updatedTx ->
                viewModel.updateTransaction(entity, updatedTx)
                transactionToEdit = null
            },
            onPurge = { txId ->
                val updated = payload.transactions.filter { it.id != txId }
                viewModel.updateBurnRatePayload(entity, payload.copy(transactions = updated))
                transactionToEdit = null
            }
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TransactionEditSheet(
    tx: Transaction,
    tags: List<String>,
    onDismiss: () -> Unit,
    onSave: (Transaction) -> Unit,
    onPurge: (String) -> Unit
) {
    ModalBottomSheet(onDismissRequest = onDismiss) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 8.dp)
                .verticalScroll(rememberScrollState()),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text("Edit Transaction", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
            Spacer(Modifier.height(16.dp))
            
            var editAmt by remember { mutableStateOf(tx.amount.toString()) }
            var editTag by remember { mutableStateOf(tx.tag) }
            
            val txZdt = java.time.Instant.ofEpochMilli(tx.timestampEpoch).atZone(java.time.ZoneId.systemDefault())
            
            val hoursList = remember { (0..23).map { it.toString().padStart(2, '0') } }
            val minutesList = remember { (0..59).map { it.toString().padStart(2, '0') } }
            val daysList = remember { (1..31).map { it.toString().padStart(2, '0') } }
            val monthsList = remember { (1..12).map { it.toString().padStart(2, '0') } }
            val yearsList = remember { (2020..2030).map { it.toString() } }
            
            var selHour by remember { mutableStateOf(txZdt.hour.toString().padStart(2, '0')) }
            var selMinute by remember { mutableStateOf(txZdt.minute.toString().padStart(2, '0')) }
            var selDay by remember { mutableStateOf(txZdt.dayOfMonth.toString().padStart(2, '0')) }
            var selMonth by remember { mutableStateOf(txZdt.monthValue.toString().padStart(2, '0')) }
            var selYear by remember { mutableStateOf(txZdt.year.toString()) }

            Text("AMOUNT", style = MaterialTheme.typography.labelSmall)
            Text(
                text = if (editAmt.isEmpty()) "₹0.00" else "₹$editAmt",
                style = MaterialTheme.typography.headlineMedium,
                fontFamily = FontFamily.Monospace,
                color = MaterialTheme.colorScheme.primary
            )
            
            // Compact numpad
            val keys = listOf("1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "0", "DEL")
            LazyVerticalGrid(
                columns = GridCells.Fixed(3),
                modifier = Modifier
                    .fillMaxWidth()
                    .heightIn(max = 200.dp) // constrained height for sheet
                    .padding(vertical = 8.dp)
            ) {
                items(keys) { key ->
                    Box(
                        modifier = Modifier
                            .aspectRatio(2f)
                            .padding(4.dp)
                            .background(MaterialTheme.colorScheme.surfaceVariant, MaterialTheme.shapes.small)
                            .clickable {
                                if (key == "DEL") {
                                    if (editAmt.isNotEmpty()) editAmt = editAmt.dropLast(1)
                                } else if (key == ".") {
                                    if (!editAmt.contains(".")) editAmt += "."
                                } else {
                                    if (editAmt.contains(".") && editAmt.substringAfter(".", "").length >= 2) {
                                        // block
                                    } else {
                                        editAmt += key
                                    }
                                }
                            },
                        contentAlignment = Alignment.Center
                    ) {
                        Text(key, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                    }
                }
            }

            Spacer(Modifier.height(16.dp))
            Text("TAG", style = MaterialTheme.typography.labelSmall)
            LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                items(tags) { t ->
                    FilterChip(
                        selected = editTag == t,
                        onClick = { editTag = t },
                        label = { Text(t) }
                    )
                }
            }

            Spacer(Modifier.height(16.dp))
            Text("DATE & TIME", style = MaterialTheme.typography.labelSmall)
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) {
                TerminalWheelPicker(items = daysList, initialSelection = selDay, onItemSelected = { selDay = it })
                TerminalWheelPicker(items = monthsList, initialSelection = selMonth, onItemSelected = { selMonth = it })
                TerminalWheelPicker(items = yearsList, initialSelection = selYear, onItemSelected = { selYear = it })
                Text(" - ", modifier = Modifier.align(Alignment.CenterVertically))
                TerminalWheelPicker(items = hoursList, initialSelection = selHour, onItemSelected = { selHour = it })
                TerminalWheelPicker(items = minutesList, initialSelection = selMinute, onItemSelected = { selMinute = it })
            }

            Spacer(Modifier.height(24.dp))
            Button(
                onClick = {
                    val finalAmt = editAmt.toDoubleOrNull() ?: 0.0
                    val ldt = java.time.LocalDateTime.of(
                        selYear.toInt(), selMonth.toInt(), selDay.toInt(),
                        selHour.toInt(), selMinute.toInt()
                    )
                    val epoch = ldt.atZone(java.time.ZoneId.systemDefault()).toInstant().toEpochMilli()
                    onSave(tx.copy(amount = finalAmt, tag = editTag, timestampEpoch = epoch))
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("SAVE CHANGES", fontWeight = FontWeight.Bold)
            }
            Spacer(Modifier.height(8.dp))
            OutlinedButton(
                onClick = { onPurge(tx.id) },
                modifier = Modifier.fillMaxWidth(),
                colors = ButtonDefaults.outlinedButtonColors(contentColor = MaterialTheme.colorScheme.error)
            ) {
                Text("[ PURGE ]", fontWeight = FontWeight.Bold)
            }
            Spacer(Modifier.height(24.dp))
        }
    }
}

@Composable
fun ScrollToLatestButton(
    visible: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    androidx.compose.animation.AnimatedVisibility(
        visible = visible,
        modifier = modifier
    ) {
        Box(
            modifier = Modifier
                .size(48.dp)
                .background(MaterialTheme.colorScheme.surfaceVariant, RectangleShape)
                .border(2.dp, MaterialTheme.colorScheme.outline, RectangleShape)
                .clickable { onClick() },
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = Icons.Default.KeyboardArrowDown,
                contentDescription = "Jump to Latest",
                tint = MaterialTheme.colorScheme.onSurface
            )
        }
    }
}
"""

with open("app/src/main/java/com/example/ui/screens/BurnRateTrackerUI.kt", "w") as f:
    f.write(new_code)
