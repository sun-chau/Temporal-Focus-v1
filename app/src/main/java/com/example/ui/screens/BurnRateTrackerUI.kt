package com.example.ui.screens

import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.GridItemSpan
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.*
import com.example.viewmodel.TrackerViewModel
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.UUID

@OptIn(ExperimentalFoundationApi::class)
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

    val tags = listOf("GENERAL", "FOOD", "TRANSPORT") + payload.customTags.toList()
    if (selectedTag !in tags) {
        selectedTag = "GENERAL"
    }

    val currentMonth = java.time.YearMonth.now()
    val monthlySum = payload.transactions.filter {
        val dateTime = java.time.Instant.ofEpochMilli(it.timestampEpoch).atZone(java.time.ZoneId.systemDefault()).toLocalDate()
        java.time.YearMonth.from(dateTime) == currentMonth
    }.sumOf { it.amount }

    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        // Top Fraction
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(
                text = "₹%.2f / ₹%.2f".format(monthlySum, payload.monthlyLimit),
                style = MaterialTheme.typography.displaySmall,
                fontWeight = FontWeight.Bold,
                fontFamily = FontFamily.Monospace,
                color = if (payload.monthlyLimit > 0.0 && monthlySum > payload.monthlyLimit) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.onSurface
            )
            IconButton(onClick = { showLimitDialog = true }) {
                Icon(Icons.Filled.Edit, contentDescription = "Edit Limit")
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        // Input Display
        Text(
            text = if (inputStr.isEmpty()) "₹0.00" else "₹$inputStr",
            style = MaterialTheme.typography.displayMedium,
            fontFamily = FontFamily.Monospace,
            modifier = Modifier.fillMaxWidth(),
            textAlign = TextAlign.Center,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )

        Spacer(modifier = Modifier.height(16.dp))

        // Tags
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .horizontalScroll(rememberScrollState()),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            tags.forEach { tag ->
                FilterChip(
                    selected = selectedTag == tag,
                    onClick = { selectedTag = tag },
                    label = { Text(tag) }
                )
            }
            FilterChip(
                selected = false,
                onClick = { showAddTagDialog = true },
                label = { Text("+ TAG") }
            )
        }

        Spacer(modifier = Modifier.height(8.dp))
        HorizontalDivider()
        Spacer(modifier = Modifier.height(8.dp))

        // Ledger
        val dateFormat = SimpleDateFormat("dd MMM, HH:mm", Locale.getDefault())
        LazyColumn(
            modifier = Modifier.weight(1f),
            reverseLayout = true
        ) {
            items(payload.transactions, key = { it.id }) { tx ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .combinedClickable(
                            onClick = {},
                            onLongClick = {
                                val updated = payload.transactions.filter { it.id != tx.id }
                                viewModel.updateBurnRatePayload(entity, payload.copy(transactions = updated))
                            }
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
                                }
                            } else if (key == "DEL") {
                                if (inputStr.isNotEmpty()) inputStr = inputStr.dropLast(1)
                            } else if (key == ".") {
                                if (!inputStr.contains(".")) inputStr += "."
                            } else {
                                inputStr += key
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

    if (showLimitDialog) {
        var limitInput by remember { mutableStateOf(payload.monthlyLimit.toString()) }
        AlertDialog(
            onDismissRequest = { showLimitDialog = false },
            title = { Text("Set Monthly Limit") },
            text = {
                OutlinedTextField(
                    value = limitInput,
                    onValueChange = { limitInput = it },
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
            },
            confirmButton = {
                TextButton(
                    onClick = {
                        val limit = limitInput.toDoubleOrNull() ?: 0.0
                        viewModel.updateBurnRatePayload(entity, payload.copy(monthlyLimit = limit))
                        showLimitDialog = false
                    }
                ) { Text("SAVE") }
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
                TextButton(
                    onClick = {
                        if (newTagInput.isNotBlank()) {
                            viewModel.addBurnRateTag(entity, newTagInput)
                        }
                        showAddTagDialog = false
                    }
                ) { Text("SAVE") }
            },
            dismissButton = {
                TextButton(onClick = { showAddTagDialog = false }) { Text("CANCEL") }
            }
        )
    }
}
