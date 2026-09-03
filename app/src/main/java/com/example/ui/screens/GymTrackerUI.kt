package com.example.ui.screens

import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.RectangleShape
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.*
import com.example.viewmodel.TrackerViewModel
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.UUID

@Composable
fun GymTrackerUI(entity: TrackerEntity, payload: GymPayload, viewModel: TrackerViewModel) {
    var addingToSessionId by remember { mutableStateOf<String?>(null) }
    var editingExercise by remember { mutableStateOf<Pair<String, ExerciseLog>?>(null) } // sessionId to ExerciseLog

    val sortedRoutines = payload.routines.sortedByDescending { it.dateEpoch }
    val formatter = SimpleDateFormat("dd MMM yyyy - HH:mm", Locale.getDefault())

    val historicalExercises = remember(payload) {
        payload.routines.flatMap { it.exercises }.map { it.name }.toSet()
    }

    Column(modifier = Modifier.fillMaxSize()) {
        OutlinedButton(
            onClick = {
                val newSession = WorkoutSession(dateEpoch = System.currentTimeMillis())
                val newRoutines = payload.routines + newSession
                viewModel.updateGymPayload(entity, payload.copy(routines = newRoutines))
            },
            shape = RectangleShape,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("START NEW SESSION")
        }

        Spacer(Modifier.height(16.dp))
        LazyColumn(modifier = Modifier.weight(1f)) {
            items(sortedRoutines) { session ->
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 8.dp)
                        .border(1.dp, MaterialTheme.colorScheme.outline, RectangleShape)
                        .padding(16.dp)
                ) {
                    Text(
                        formatter.format(Date(session.dateEpoch)),
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.primary
                    )
                    Spacer(Modifier.height(8.dp))

                    session.exercises.forEach { ex ->
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 4.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text("> ${ex.name}", fontFamily = FontFamily.Monospace, fontWeight = FontWeight.Bold)
                                when (ex.type) {
                                    ExerciseType.REPS_ONLY -> {
                                        ex.sets.forEachIndexed { i, set ->
                                            val w = set.weightKg?.let { " @ ${it}kg" } ?: ""
                                            Text("  Set ${i+1}: ${set.reps} reps$w", fontFamily = FontFamily.Monospace, style = MaterialTheme.typography.bodyMedium)
                                        }
                                    }
                                    ExerciseType.TIMED_DISTANCE -> {
                                        val m = (ex.durationSeconds ?: 0) / 60
                                        val s = (ex.durationSeconds ?: 0) % 60
                                        Text("  ${ex.distanceMeters ?: 0}M : ${m}m ${s}s", fontFamily = FontFamily.Monospace, style = MaterialTheme.typography.bodyMedium)
                                    }
                                    ExerciseType.STATIC_HOLD -> {
                                        Text("  ${ex.durationSeconds ?: 0}s HOLD", fontFamily = FontFamily.Monospace, style = MaterialTheme.typography.bodyMedium)
                                    }
                                }
                            }
                            IconButton(onClick = { editingExercise = Pair(session.id, ex) }) {
                                Icon(Icons.Default.Edit, contentDescription = "Edit")
                            }
                            IconButton(onClick = { viewModel.deleteExercise(entity, session.id, ex.id) }) {
                                Icon(Icons.Default.Delete, contentDescription = "Delete")
                            }
                        }
                    }

                    Spacer(Modifier.height(16.dp))
                    OutlinedButton(
                        onClick = { addingToSessionId = session.id },
                        shape = RectangleShape,
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text("+ LOG EXERCISE")
                    }
                }
            }
        }
    }

    if (addingToSessionId != null) {
        GymExerciseSheet(
            historicalExercises = historicalExercises,
            initialExercise = null,
            onDismiss = { addingToSessionId = null },
            onSave = { newEx ->
                val newRoutines = payload.routines.map { s ->
                    if (s.id == addingToSessionId) s.copy(exercises = s.exercises + newEx) else s
                }
                viewModel.updateGymPayload(entity, payload.copy(routines = newRoutines))
                addingToSessionId = null
            }
        )
    }

    editingExercise?.let { (sessionId, ex) ->
        GymExerciseSheet(
            historicalExercises = historicalExercises,
            initialExercise = ex,
            onDismiss = { editingExercise = null },
            onSave = { updatedEx ->
                viewModel.updateExercise(entity, sessionId, updatedEx)
                editingExercise = null
            }
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun GymExerciseSheet(
    historicalExercises: Set<String>,
    initialExercise: ExerciseLog?,
    onDismiss: () -> Unit,
    onSave: (ExerciseLog) -> Unit
) {
    var name by remember { mutableStateOf(initialExercise?.name ?: "") }
    var type by remember { mutableStateOf(initialExercise?.type ?: ExerciseType.REPS_ONLY) }

    // For simplicity, we just edit/add the first set in this UI if REPS_ONLY
    var repsStr by remember { mutableStateOf(initialExercise?.sets?.firstOrNull()?.reps?.toString() ?: "") }
    var weightStr by remember { mutableStateOf(initialExercise?.sets?.firstOrNull()?.weightKg?.toString() ?: "") }

    var distanceStr by remember { mutableStateOf(initialExercise?.distanceMeters?.toString() ?: "") }
    var durationStr by remember { mutableStateOf(initialExercise?.durationSeconds?.toString() ?: "") }

    var activeField by remember { mutableStateOf(if (type == ExerciseType.REPS_ONLY) "REPS" else "DISTANCE") }

    ModalBottomSheet(onDismissRequest = onDismiss) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
                .padding(bottom = 32.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            if (historicalExercises.isNotEmpty()) {
                LazyRow(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(historicalExercises.toList()) { exName ->
                        FilterChip(
                            selected = name == exName,
                            onClick = { name = exName },
                            label = { Text("[ $exName ]", fontFamily = FontFamily.Monospace) }
                        )
                    }
                }
            }

            OutlinedTextField(
                value = name,
                onValueChange = { name = it },
                label = { Text("Exercise Name (e.g. Pushups)") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true
            )

            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState()),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                ExerciseType.values().forEach { t ->
                    FilterChip(
                        selected = type == t,
                        onClick = {
                            type = t
                            activeField = when (t) {
                                ExerciseType.REPS_ONLY -> "REPS"
                                ExerciseType.TIMED_DISTANCE -> "DISTANCE"
                                ExerciseType.STATIC_HOLD -> "DURATION"
                            }
                        },
                        label = { Text(t.name.replace("_", " ")) }
                    )
                }
            }

            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                when (type) {
                    ExerciseType.REPS_ONLY -> {
                        MetricBox("REPS", repsStr, activeField == "REPS", Modifier.weight(1f)) { activeField = "REPS" }
                        MetricBox("WEIGHT (KG)", weightStr, activeField == "WEIGHT", Modifier.weight(1f)) { activeField = "WEIGHT" }
                    }
                    ExerciseType.TIMED_DISTANCE -> {
                        MetricBox("DISTANCE (M)", distanceStr, activeField == "DISTANCE", Modifier.weight(1f)) { activeField = "DISTANCE" }
                        MetricBox("DURATION (S)", durationStr, activeField == "DURATION", Modifier.weight(1f)) { activeField = "DURATION" }
                    }
                    ExerciseType.STATIC_HOLD -> {
                        MetricBox("DURATION (S)", durationStr, activeField == "DURATION", Modifier.weight(1f)) { activeField = "DURATION" }
                    }
                }
            }

            val keys = listOf("1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "0", "DEL", "DONE")
            LazyVerticalGrid(
                columns = GridCells.Fixed(3),
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(keys) { key ->
                    Button(
                        onClick = {
                            if (key == "DONE") {
                                if (name.isNotBlank()) {
                                    val sets = if (type == ExerciseType.REPS_ONLY) {
                                        listOf(ExerciseSet(
                                            id = initialExercise?.sets?.firstOrNull()?.id ?: UUID.randomUUID().toString(),
                                            reps = repsStr.toIntOrNull() ?: 0,
                                            weightKg = weightStr.toFloatOrNull()
                                        ))
                                    } else {
                                        emptyList()
                                    }

                                    val ex = ExerciseLog(
                                        id = initialExercise?.id ?: UUID.randomUUID().toString(),
                                        name = name,
                                        type = type,
                                        sets = sets,
                                        distanceMeters = if (type == ExerciseType.TIMED_DISTANCE) distanceStr.toIntOrNull() else null,
                                        durationSeconds = if (type == ExerciseType.TIMED_DISTANCE || type == ExerciseType.STATIC_HOLD) durationStr.toIntOrNull() else null
                                    )
                                    onSave(ex)
                                }
                            } else if (key == "DEL") {
                                when (activeField) {
                                    "REPS" -> if (repsStr.isNotEmpty()) repsStr = repsStr.dropLast(1)
                                    "WEIGHT" -> if (weightStr.isNotEmpty()) weightStr = weightStr.dropLast(1)
                                    "DISTANCE" -> if (distanceStr.isNotEmpty()) distanceStr = distanceStr.dropLast(1)
                                    "DURATION" -> if (durationStr.isNotEmpty()) durationStr = durationStr.dropLast(1)
                                }
                            } else {
                                when (activeField) {
                                    "REPS" -> repsStr += key
                                    "WEIGHT" -> weightStr += key
                                    "DISTANCE" -> distanceStr += key
                                    "DURATION" -> durationStr += key
                                }
                            }
                        },
                        modifier = Modifier.aspectRatio(if (key == "DONE") 3f else 2f),
                        shape = RectangleShape,
                        colors = if (key == "DONE") ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary) else ButtonDefaults.filledTonalButtonColors()
                    ) {
                        Text(key, fontWeight = FontWeight.Bold, fontSize = 20.sp)
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MetricBox(label: String, value: String, isActive: Boolean, modifier: Modifier = Modifier, onClick: () -> Unit) {
    Column(
        modifier = modifier
            .border(if (isActive) 2.dp else 1.dp, if (isActive) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outline, RectangleShape)
            .clickable { onClick() }
            .padding(16.dp)
    ) {
        Text(label, style = MaterialTheme.typography.labelSmall, color = if (isActive) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface)
        Text(if (value.isEmpty()) "0" else value, fontFamily = FontFamily.Monospace, style = MaterialTheme.typography.headlineMedium)
    }
}
