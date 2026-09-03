with open("app/src/main/java/com/example/viewmodel/TrackerViewModel.kt", "w") as f:
    f.write("""package com.example.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.*
import com.google.gson.Gson
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class TrackerViewModel(application: Application) : AndroidViewModel(application) {
    private val trackerDao = AppDatabase.getDatabase(application).trackerDao()
    private val gson = Gson()
    val trackers: StateFlow<List<TrackerEntity>> = trackerDao.getAllTrackers().stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
    
    fun getParsedPayload(entity: TrackerEntity): Any? {
        return try {
            val json = if (entity.payloadData.isBlank() || entity.payloadData == "{}") null else entity.payloadData
            when (entity.type) {
                TrackerType.GYM -> json?.let { gson.fromJson(it, GymPayload::class.java) } ?: GymPayload()
                TrackerType.SYLLABUS -> json?.let { gson.fromJson(it, SyllabusPayload::class.java) } ?: SyllabusPayload()
                TrackerType.CUSTOM -> json?.let { gson.fromJson(it, CustomPayload::class.java) } ?: CustomPayload()
                TrackerType.ASSIGNMENT -> json?.let { gson.fromJson(it, AssignmentPayload::class.java) } ?: AssignmentPayload()
            }
        } catch (e: Exception) {
            null
        }
    }

    fun updateGymPayload(entity: TrackerEntity, payload: GymPayload) {
        val newData = gson.toJson(payload)
        updateTracker(entity.copy(payloadData = newData, lastModified = System.currentTimeMillis()))
    }

    fun updateSyllabusPayload(entity: TrackerEntity, payload: SyllabusPayload) {
        val newData = gson.toJson(payload)
        updateTracker(entity.copy(payloadData = newData, lastModified = System.currentTimeMillis()))
    }

    fun updateCustomPayload(entity: TrackerEntity, payload: CustomPayload) {
        val newData = gson.toJson(payload)
        updateTracker(entity.copy(payloadData = newData, lastModified = System.currentTimeMillis()))
    }

    fun updateAssignmentPayload(entity: TrackerEntity, payload: AssignmentPayload) {
        val newData = gson.toJson(payload)
        updateTracker(entity.copy(payloadData = newData, lastModified = System.currentTimeMillis()))
    }

    fun insertTracker(tracker: TrackerEntity) {
        viewModelScope.launch(Dispatchers.IO) {
            trackerDao.insertTracker(tracker)
        }
    }

    fun updateTracker(tracker: TrackerEntity) {
        viewModelScope.launch(Dispatchers.IO) {
            trackerDao.updateTracker(tracker)
        }
    }

    fun deleteTracker(tracker: TrackerEntity) {
        viewModelScope.launch(Dispatchers.IO) {
            trackerDao.deleteTracker(tracker)
        }
    }
}
""")
