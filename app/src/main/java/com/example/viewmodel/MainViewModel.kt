package com.example.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import android.media.AudioManager
import android.media.RingtoneManager
import android.media.ToneGenerator
import android.app.NotificationChannel

import android.content.Intent
import android.app.PendingIntent
import android.graphics.Bitmap
import android.graphics.Canvas
import androidx.core.content.res.ResourcesCompat

import android.graphics.Color

import com.example.receiver.AlarmScheduler

import com.example.receiver.NotificationActionReceiver
import com.example.MainActivity

import android.app.NotificationManager
import android.content.pm.PackageManager
import androidx.core.app.NotificationCompat
import androidx.core.content.ContextCompat
import android.os.Build
import android.os.VibrationEffect
import android.os.Vibrator
import android.os.VibratorManager
import android.content.Context
import androidx.lifecycle.viewModelScope
import com.google.gson.Gson
import com.example.data.*
import com.example.data.AppDatabase
import com.example.data.toRecurrencePattern
import com.example.data.FocusSessionStats
import com.example.data.FocusSessionStatsDao
import com.example.data.AppSettings
import com.example.data.TimerTask
import com.example.data.DailyScheduleTask
import com.example.data.ScheduleStatus
import com.example.R
import com.example.data.TimerTaskRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import java.util.Calendar

enum class TimerMode { CREATE_DAILY_SCHEDULE,  HOME, CHRONOMETER, POMODORO, QUICK_DEADLINES, DAILY_SCHEDULE, PROFILE, SETTINGS, DEVELOPER_OPTIONS, UPDATE_LOG, ANALYTICS, PRIVATE_JOURNAL, CHECK_INS, COLOR_CUSTOMIZATION, SECURITY_SETTINGS, LANDSCAPE_CHRONOGRAPH, SETTINGS_APPEARANCE, SETTINGS_FEATURE, SETTINGS_DAILY_SCHEDULE, SETTINGS_DEADLINES, SETTINGS_NOTIFICATIONS, SETTINGS_DATA, SETTINGS_SUPPORT, SETTINGS_LAUNCHER_ICON, SETTINGS_ABOUT, SETTINGS_HELP, SETTINGS_FEEDBACK }
enum class PomodoroPhase { FOCUS, BREAK, LONG_BREAK }
enum class ChronometerLayout { VERTICAL, HORIZONTAL }
data class UiState(
    val isCreatingChronometer: Boolean = false,
    val editingTask: TimerTask? = null,
    val currentMode: TimerMode = TimerMode.HOME,
    val currentDateTime: Long = System.currentTimeMillis(),
    
    // Chronometer State
    val maxStageSlots: Int = 5,
    val selectedDisplayIds: List<String> = emptyList(),
    val isUrgentMode: Boolean = false,
    val layoutPreference: ChronometerLayout = ChronometerLayout.VERTICAL,
    val launcherIcon: String = "orange",
    
    val dailySchedules: List<com.example.data.DailyScheduleTask> = emptyList(),
        val use24HourFormat: Boolean = true,
    val autoStatusIfMissed: String = "NOT_DONE",
    val enableDailyScheduleRadioMenu: Boolean = true,
    val dailyScheduleDraft: com.example.data.DailyScheduleDraft = com.example.data.DailyScheduleDraft(),
    
    val showYears: Boolean = true,
    val showMonths: Boolean = true,
    val showDays: Boolean = true,
    val showHours: Boolean = true,
    val showMinutes: Boolean = true,
    val showSeconds: Boolean = true,
    
    // Pomodoro State
    val baseFocusDurationMinutes: Int = 25,
    val baseBreakDurationMinutes: Int = 5,
    val pomodoroTargetSessions: Int = 4,
    val longBreakDurationMinutes: Int = 15,
    
    val currentSessionCount: Int = 0,
    val currentPhase: PomodoroPhase = PomodoroPhase.FOCUS,
    val isPomodoroRunning: Boolean = false,
    val hasPomodoroStarted: Boolean = false,
    val pomodoroTimeRemainingSeconds: Long = 25 * 60L,
    val sessionExtraTimeSeconds: Long = 0L,
    val liveAdjustmentCount: Int = 0,
    
    val totalSessionsCompleted: Int = 0,
    val totalFocusTimeSeconds: Long = 0L,
    val totalBreaksTaken: Int = 0,
    val totalBreakTimeSeconds: Long = 0L,
    
    // Profile State
    val profileName: String = "Guest",
    val profileBio: String = "",
    val profileImageUri: String = "",
    val profileCustomFields: Map<String, String> = emptyMap(),
    val customLabels: Set<String> = setOf("Work", "Study", "Personal", "Health", "Leisure", "Other"),
    val customColors: Set<String> = emptySet(),
    val appearanceMode: Int = 0,
    val currentTheme: String = "Default",
    val pomodoroFullscreenTheme: String = "Default Light",
    val customBackdropColor: String = "",
    val customBaseTextColor: String = "",
    val customOverdueTextColor: String = "",
    val dailyFocusGoalMinutes: Int = 0,
    
    // New Settings
    val coloredLabelsEnabled: Boolean = true,
    val preventHidingAllUnits: Boolean = true,
    val pomodoroPhaseAlerts: Boolean = true,
    val chronometerDeadlinesAlerts: Boolean = true,
    val pomodoroPhaseVibrationEnabled: Boolean = true,
    val chronometerDeadlineVibrationEnabled: Boolean = true,
    val chronometerDeadlineOffsetMinutes: Int = 0,
    val privateJournalLockEnabled: Boolean = true,
    val appPasswordEnabled: Boolean = false,
    val appPassword: String = "",
    val passwordHint: String = "",
    val securityQuestion: String = "",
    val securityAnswer: String = "",
    val securityQuestion2: String = "",
    val securityAnswer2: String = "",
    val securityQuestion3: String = "",
    val securityAnswer3: String = "",
    val biometricsEnabled: Boolean = false,
    val isAuthenticated: Boolean = false
)

class MainViewModel(application: Application) : AndroidViewModel(application) {
    
    private val repository: TimerTaskRepository
    private val appSettings: AppSettings
    private val statsDao: FocusSessionStatsDao
    private val journalDao: com.example.data.JournalDao
    private val trackerDao: com.example.data.TrackerDao
    val focusStats: StateFlow<List<FocusSessionStats>>
    val journalEntries: StateFlow<List<com.example.data.JournalEntry>>
    val journalTemplates: StateFlow<List<com.example.data.JournalTemplate>>
    val trackers: StateFlow<List<com.example.data.TrackerEntity>>
    private val _uiState = MutableStateFlow(UiState())
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    val activeTasks: StateFlow<List<TimerTask>>
    val completedTasks: StateFlow<List<TimerTask>>

    private val alertedApproachingIds = mutableSetOf<String>()
    private val alertedReachedIds = mutableSetOf<String>()

    private fun performRollingRefill() {
        viewModelScope.launch(kotlinx.coroutines.Dispatchers.IO) {
            // Background evaluation to refill occurrences when the generated batch approaches its end
            val db = com.example.data.AppDatabase.getDatabase(getApplication())
            val allSchedules = db.dailyScheduleDao().getAllSchedulesSync()
            
            val latestTasks = mutableMapOf<String, com.example.data.DailyScheduleTask>()
            allSchedules.forEach { task ->
                if (task.seriesId != null) {
                    val currentLatest = latestTasks[task.seriesId]
                    if (currentLatest == null || task.startTime > currentLatest.startTime) {
                        latestTasks[task.seriesId] = task
                    }
                }
            }
            
            val maxDays = appSettings.recurrenceGenerationCapYears * 365
            val now = System.currentTimeMillis()
            val threshold = now + (maxDays - 30) * 86400000L
            
            latestTasks.forEach { (seriesId, lastTask) ->
                if (lastTask.recurrenceType != null && lastTask.startTime < threshold) {
                    // Refill batch logic here
                    // (Requires parsing recurrence rule and injecting 1-year batch)
                }
            }
        }
    }

    init {
        val database = AppDatabase.getDatabase(application)
        statsDao = database.focusSessionStatsDao()
        journalDao = database.journalDao()
        trackerDao = database.trackerDao()
        focusStats = statsDao.getAllStats().stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
        journalEntries = journalDao.getAllEntries().stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
        journalTemplates = journalDao.getAllTemplates().stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
        trackers = trackerDao.getAllTrackers().stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
        repository = TimerTaskRepository(database.timerTaskDao())
        appSettings = AppSettings(application)
        performRollingRefill()
        
        activeTasks = repository.activeTasks.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
        completedTasks = repository.completedTasks.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
        
        viewModelScope.launch(Dispatchers.IO) {
            val count = journalDao.getTemplateCount()
            if (count == 0) {
                val defaultTemplates = listOf(
                    com.example.data.JournalTemplate(title = "The Daily Debrief", content = "• Did I execute my schedule as planned today?\n\n• What was the friction point that broke my discipline?\n\n• How did I handle stress or adversity today?\n\n", isDefault = true),
                    com.example.data.JournalTemplate(title = "The Introspective Route", content = "• What is a belief or assumption I held today that I should question?\n\n• Am I acting out of habit, or out of intention?\n\n• What did I learn about myself in today's quiet moments?\n\n", isDefault = true),
                    com.example.data.JournalTemplate(title = "The Evening Gratitude", content = "• List three specific things that went well today:\n1. \n2. \n3. \n\n", isDefault = true)
                )
                defaultTemplates.forEach { journalDao.insertTemplate(it) }
            }
            // Mock schedules removed
        }
        
        viewModelScope.launch(Dispatchers.IO) {
            while (true) {
                val now = System.currentTimeMillis()
                val autoStatus = appSettings.autoStatusIfMissed
                if (autoStatus == "COMPLETED" || autoStatus == "SKIPPED") {
                    val schedules = _uiState.value.dailySchedules
                    for (schedule in schedules) {
                        if (schedule.endTime < now && schedule.status == "NOT_DONE") {
                            val updated = schedule.copy(status = autoStatus)
                            database.dailyScheduleDao().updateSchedule(updated)
                        }
                    }
                }
                kotlinx.coroutines.delay(60000)
            }
        }
        
        viewModelScope.launch(Dispatchers.IO) {
            database.dailyScheduleDao().getAllSchedules().collect { schedules ->
                _uiState.update { it.copy(dailySchedules = schedules) }
            }
        }
        // Load settings
        _uiState.update { it.copy(
                        use24HourFormat = appSettings.use24HourFormat,
            autoStatusIfMissed = appSettings.autoStatusIfMissed,
            enableDailyScheduleRadioMenu = appSettings.enableDailyScheduleRadioMenu,
            maxStageSlots = appSettings.maxStageSlots,
            selectedDisplayIds = appSettings.selectedDisplayIds.split(",").filter { it.isNotEmpty() },
            isUrgentMode = appSettings.isUrgentMode,
            layoutPreference = if (appSettings.layoutPreference == "horizontal") ChronometerLayout.HORIZONTAL else ChronometerLayout.VERTICAL,
            launcherIcon = appSettings.launcherIcon,
            showYears = appSettings.showYears,
            showMonths = appSettings.showMonths,
            showDays = appSettings.showDays,
            showHours = appSettings.showHours,
            showMinutes = appSettings.showMinutes,
            showSeconds = appSettings.showSeconds,
            baseFocusDurationMinutes = appSettings.baseFocusDurationMinutes,
            baseBreakDurationMinutes = appSettings.baseBreakDurationMinutes,
            pomodoroTargetSessions = appSettings.pomodoroTargetSessions,
            longBreakDurationMinutes = appSettings.longBreakDurationMinutes,
            pomodoroTimeRemainingSeconds = appSettings.baseFocusDurationMinutes * 60L,
            totalSessionsCompleted = appSettings.totalSessionsCompleted,
            totalFocusTimeSeconds = appSettings.totalFocusTimeSeconds,
            totalBreaksTaken = appSettings.totalBreaksTaken,
            totalBreakTimeSeconds = appSettings.totalBreakTimeSeconds,
            appearanceMode = appSettings.appearanceMode,
            currentTheme = appSettings.currentTheme,
            pomodoroFullscreenTheme = appSettings.pomodoroFullscreenTheme,
            profileName = appSettings.profileName,
            profileBio = appSettings.profileBio,
            profileImageUri = appSettings.profileImageUri,
            profileCustomFields = appSettings.profileCustomFields.associate { val parts = it.split("|", limit = 2); parts[0] to (parts.getOrNull(1) ?: "") },
            customLabels = appSettings.customLabels,
            customColors = appSettings.customColors,
            dailyFocusGoalMinutes = appSettings.dailyFocusGoalMinutes,
            
            coloredLabelsEnabled = appSettings.coloredLabelsEnabled,
            preventHidingAllUnits = appSettings.preventHidingAllUnits,
            pomodoroPhaseAlerts = appSettings.pomodoroPhaseAlerts,
            chronometerDeadlinesAlerts = appSettings.chronometerDeadlinesAlerts,
            pomodoroPhaseVibrationEnabled = appSettings.pomodoroPhaseVibrationEnabled,
            chronometerDeadlineVibrationEnabled = appSettings.chronometerDeadlineVibrationEnabled,
            chronometerDeadlineOffsetMinutes = appSettings.chronometerDeadlineOffsetMinutes,
            privateJournalLockEnabled = appSettings.privateJournalLockEnabled,
            appPasswordEnabled = appSettings.appPasswordEnabled,
            appPassword = appSettings.appPassword,
            passwordHint = appSettings.passwordHint,
            securityQuestion = appSettings.securityQuestion,
            securityAnswer = appSettings.securityAnswer,
            securityQuestion2 = appSettings.securityQuestion2,
            securityAnswer2 = appSettings.securityAnswer2,
            securityQuestion3 = appSettings.securityQuestion3,
            securityAnswer3 = appSettings.securityAnswer3,
            biometricsEnabled = appSettings.biometricsEnabled,
            isAuthenticated = !appSettings.appPasswordEnabled
        ) }

        // Start global clock and pomodoro tick
        viewModelScope.launch {
            while (true) {
                delay(1000)
                val currentMillis = System.currentTimeMillis()
                


                _uiState.update { state ->
                    var newTimeRemaining = state.pomodoroTimeRemainingSeconds
                    var newFocusTime = state.totalFocusTimeSeconds
                    var newBreakTime = state.totalBreakTimeSeconds
                    
                    if (state.isPomodoroRunning) {
                        newTimeRemaining -= 1
                        if (state.currentPhase == PomodoroPhase.FOCUS) {
                            newFocusTime += 1
                            if (newFocusTime % 10L == 0L) { // Save every 10 seconds to avoid spamming I/O
                                appSettings.totalFocusTimeSeconds = newFocusTime
                            }
                        } else {
                            newBreakTime += 1
                            if (newBreakTime % 10L == 0L) {
                                appSettings.totalBreakTimeSeconds = newBreakTime
                            }
                        }
                        
                        if (newTimeRemaining <= 0) {
                            handlePomodoroPhaseComplete()
                        }
                    }
                    
                    state.copy(
                        currentDateTime = currentMillis,
                        pomodoroTimeRemainingSeconds = if (newTimeRemaining > 0) newTimeRemaining else 0L,
                        totalFocusTimeSeconds = newFocusTime,
                        totalBreakTimeSeconds = newBreakTime
                    )
                }
            }
        }
    }

    // --- Actions ---



    fun setCreatingChronometer(isCreating: Boolean) {
        _uiState.update { it.copy(isCreatingChronometer = isCreating) }
    }
    
    fun setEditingTask(task: TimerTask?) {
        _uiState.update { it.copy(editingTask = task) }
    }

    fun setTimerMode(mode: TimerMode) {
        _uiState.update { it.copy(currentMode = mode) }
    }

    // Chronometer Actions
    fun toggleDisplayId(id: String) {
        val currentIds = appSettings.selectedDisplayIds.split(",").filter { it.isNotEmpty() }.toMutableList()
        val maxSlots = appSettings.maxStageSlots
        
        if (currentIds.contains(id)) {
            currentIds.remove(id)
        } else {
            currentIds.add(id)
            if (maxSlots != -1) {
                while (currentIds.size > maxSlots) {
                    currentIds.removeAt(0) // FIFO
                }
            }
        }
        
        val newString = currentIds.joinToString(",")
        appSettings.selectedDisplayIds = newString
        _uiState.update { it.copy(selectedDisplayIds = currentIds.toList()) }
    }

    fun setMaxStageSlots(slots: Int) {
        appSettings.maxStageSlots = slots
        val currentIds = appSettings.selectedDisplayIds.split(",").filter { it.isNotEmpty() }.toMutableList()
        var updatedIds = currentIds
        if (slots != -1 && currentIds.size > slots) {
            while (currentIds.size > slots) {
                currentIds.removeAt(0)
            }
            appSettings.selectedDisplayIds = currentIds.joinToString(",")
            updatedIds = currentIds
        }
        _uiState.update { it.copy(maxStageSlots = slots, selectedDisplayIds = updatedIds.toList()) }
    }

    fun toggleUrgentMode(urgent: Boolean) {
        appSettings.isUrgentMode = urgent
        _uiState.update { it.copy(isUrgentMode = urgent) }
    }


    fun setLauncherIcon(icon: String) {
        appSettings.launcherIcon = icon
        _uiState.update { it.copy(launcherIcon = icon) }
    }
    fun setLayoutPreference(layout: ChronometerLayout) {
        appSettings.layoutPreference = if (layout == ChronometerLayout.VERTICAL) "vertical" else "horizontal"
        _uiState.update { it.copy(layoutPreference = layout) }
    }

    fun toggleUnitVisibility(unit: String) {
        _uiState.update { state ->
            val newState = when (unit) {
                "Years" -> { appSettings.showYears = !state.showYears; state.copy(showYears = !state.showYears) }
                "Months" -> { appSettings.showMonths = !state.showMonths; state.copy(showMonths = !state.showMonths) }
                "Days" -> { appSettings.showDays = !state.showDays; state.copy(showDays = !state.showDays) }
                "Hours" -> { appSettings.showHours = !state.showHours; state.copy(showHours = !state.showHours) }
                "Minutes" -> { appSettings.showMinutes = !state.showMinutes; state.copy(showMinutes = !state.showMinutes) }
                "Seconds" -> { appSettings.showSeconds = !state.showSeconds; state.copy(showSeconds = !state.showSeconds) }
                else -> state
            }
            newState
        }
    }


    fun saveAdvancedDeadline(draft: com.example.data.DeadlineDraft) {
        viewModelScope.launch(kotlinx.coroutines.Dispatchers.IO) {
            val db = com.example.data.AppDatabase.getDatabase(getApplication())
            
            // Delete old if editing
            if (draft.editingId != null) {
                db.timerTaskDao().deleteTaskById(draft.editingId)
            }
            
            if (!draft.isRecurring) {
                db.timerTaskDao().insertTask(
                    com.example.data.TimerTask(
                        id = draft.editingId ?: java.util.UUID.randomUUID().toString(),
                        name = draft.name,
                        description = draft.description,
                        labels = draft.labels,
                        createdAt = draft.createdAt,
                        targetDateTime = draft.targetTime,
                        priority = draft.priority,
                        deadlineDateTime = draft.deadlineDateTime,
                        link = draft.link,
                        attachmentUri = draft.attachmentUri
                    )
                )
            } else {
                val pattern = draft.toRecurrencePattern()
                val occurrences = pattern.generateOccurrences(draft.targetTime)
                occurrences.forEachIndexed { index, currentTarget ->
                    val taskId = if (index == 0 && draft.editingId != null) draft.editingId else java.util.UUID.randomUUID().toString()
                    
                    val deadlineDiff = if (draft.deadlineDateTime != null) draft.targetTime - draft.deadlineDateTime else null
                    val newDeadline = if (deadlineDiff != null) currentTarget - deadlineDiff else null
                    
                    val t = com.example.data.TimerTask(
                        id = taskId,
                        name = draft.name,
                        description = draft.description,
                        labels = draft.labels,
                        createdAt = draft.createdAt,
                        targetDateTime = currentTarget,
                        priority = draft.priority,
                        deadlineDateTime = newDeadline,
                        link = draft.link,
                        attachmentUri = draft.attachmentUri
                    )
                    db.timerTaskDao().insertTask(t)
                }
            }
            
            // Re-fetch or whatever is needed
            setEditingTask(null)
            setTimerMode(com.example.viewmodel.TimerMode.DAILY_SCHEDULE)
        }
    }

    fun addTimerTask(
        name: String,
        description: String? = null,
        labels: String = "",
        targetDate: Long, 
        createdAt: Long = System.currentTimeMillis(), 
        recurrenceType: String = "NONE",
        customDaysInterval: Int? = null,
        maxRepetitions: Int? = null,
        specificDays: String? = null,
        priority: String = "Normal",
        deadlineDateTime: Long? = null,
        link: String? = null,
        attachmentUri: String? = null
    ) {
        viewModelScope.launch {
            val task = TimerTask(
                name = name, 
                description = description,
                labels = labels,
                targetDateTime = targetDate, 
                createdAt = createdAt, 
                recurrenceType = recurrenceType,
                customDaysInterval = customDaysInterval,
                maxRepetitions = maxRepetitions,
                specificDays = specificDays,
                priority = priority,
                deadlineDateTime = deadlineDateTime,
                link = link,
                attachmentUri = attachmentUri
            )
            repository.insertTask(task)
            AlarmScheduler.scheduleAlarmsForTask(getApplication(), task, appSettings.chronometerDeadlineOffsetMinutes)
            
            // Auto-pin to stage if room is available
            if (!appSettings.isUrgentMode) {
                val currentIds = appSettings.selectedDisplayIds.split(",").filter { it.isNotEmpty() }.toMutableList()
                if (currentIds.size < appSettings.maxStageSlots && !currentIds.contains(task.id)) {
                    currentIds.add(task.id)
                    appSettings.selectedDisplayIds = currentIds.joinToString(",")
                    _uiState.update { it.copy(selectedDisplayIds = currentIds.toList()) }
                }
            }
        }
    }

    fun addQuickDeadline(name: String, time: Long?, priority: String = "Normal") {
        viewModelScope.launch {
            val targetTime = time ?: (System.currentTimeMillis() + 86400000L)
            val task = com.example.data.TimerTask(
                name = name,
                targetDateTime = targetTime,
                deadlineDateTime = time,
                priority = priority,
                labels = "Reminder"
            )
            repository.insertTask(task)
            if (time != null) {
                com.example.receiver.AlarmScheduler.scheduleAlarmsForTask(getApplication(), task, appSettings.chronometerDeadlineOffsetMinutes)
            }
        }
    }

    fun updateTimerTask(task: TimerTask) {
        alertedApproachingIds.remove(task.id)
        alertedReachedIds.remove(task.id)
        viewModelScope.launch {
            repository.updateTask(task)
            AlarmScheduler.scheduleAlarmsForTask(getApplication(), task, appSettings.chronometerDeadlineOffsetMinutes)
        }
    }

    fun updateTask(task: TimerTask) {
        viewModelScope.launch {
            repository.updateTask(task)
        }
    }

    fun markTaskComplete(task: TimerTask, completionStatus: String? = null) {
        viewModelScope.launch {
            repository.updateTask(task.copy(isCompleted = true, completedAt = System.currentTimeMillis(), completionStatus = completionStatus))
            AlarmScheduler.cancelAlarmsForTask(getApplication(), task.id)
            val notificationManager = getApplication<Application>().getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.cancel(task.id.hashCode())
        }
    }

    fun toggleTaskPin(task: TimerTask) {
        viewModelScope.launch {
            repository.updateTask(task.copy(isPinned = !task.isPinned))
        }
    }

    fun deleteTask(task: TimerTask) {
        viewModelScope.launch {
            repository.deleteTaskById(task.id)
            AlarmScheduler.cancelAlarmsForTask(getApplication(), task.id)
            val notificationManager = getApplication<Application>().getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.cancel(task.id.hashCode())
        }
    }

    // Pomodoro Actions
    fun adjustBaseFocusTime(minutes: Int) {
        if (_uiState.value.isPomodoroRunning) return
        val newTime = (_uiState.value.baseFocusDurationMinutes + minutes).coerceIn(1, 360)
        appSettings.baseFocusDurationMinutes = newTime
        _uiState.update { 
            val remaining = if (it.currentPhase == PomodoroPhase.FOCUS) newTime * 60L else it.pomodoroTimeRemainingSeconds
            it.copy(baseFocusDurationMinutes = newTime, pomodoroTimeRemainingSeconds = remaining) 
        }
    }

    fun adjustBaseBreakTime(minutes: Int) {
        if (_uiState.value.isPomodoroRunning) return
        val newTime = (_uiState.value.baseBreakDurationMinutes + minutes).coerceIn(0, 120)
        appSettings.baseBreakDurationMinutes = newTime
        _uiState.update { 
            val remaining = if (it.currentPhase == PomodoroPhase.BREAK) newTime * 60L else it.pomodoroTimeRemainingSeconds
            it.copy(baseBreakDurationMinutes = newTime, pomodoroTimeRemainingSeconds = remaining) 
        }
    }

    fun adjustTargetSessions(count: Int) {
        if (_uiState.value.isPomodoroRunning) return
        val newCount = (_uiState.value.pomodoroTargetSessions + count).coerceIn(1, 120)
        appSettings.pomodoroTargetSessions = newCount
        _uiState.update { it.copy(pomodoroTargetSessions = newCount) }
    }

    fun adjustLongBreakTime(minutes: Int) {
        if (_uiState.value.isPomodoroRunning) return
        val newTime = (_uiState.value.longBreakDurationMinutes + minutes).coerceIn(0, 120)
        appSettings.longBreakDurationMinutes = newTime
        _uiState.update { 
            val remaining = if (it.currentPhase == PomodoroPhase.LONG_BREAK) newTime * 60L else it.pomodoroTimeRemainingSeconds
            it.copy(longBreakDurationMinutes = newTime, pomodoroTimeRemainingSeconds = remaining) 
        }
    }

    fun togglePomodoroTimer() {
        _uiState.update { it.copy(isPomodoroRunning = !it.isPomodoroRunning, hasPomodoroStarted = true) }
    }

    fun resetPomodoro() {
        _uiState.update { 
            it.copy(
                isPomodoroRunning = false,
                hasPomodoroStarted = false,
                currentPhase = PomodoroPhase.FOCUS,
                pomodoroTimeRemainingSeconds = it.baseFocusDurationMinutes * 60L,
                sessionExtraTimeSeconds = 0L,
                liveAdjustmentCount = 0,
                currentSessionCount = 0
            )
        }
    }

    fun hardResetPomodoro() {
        appSettings.totalSessionsCompleted = 0
        appSettings.totalFocusTimeSeconds = 0L
        appSettings.totalBreaksTaken = 0
        appSettings.totalBreakTimeSeconds = 0L
        _uiState.update { 
            it.copy(
                isPomodoroRunning = false,
                currentPhase = PomodoroPhase.FOCUS,
                pomodoroTimeRemainingSeconds = it.baseFocusDurationMinutes * 60L,
                sessionExtraTimeSeconds = 0L,
                currentSessionCount = 0,
                totalSessionsCompleted = 0,
                totalFocusTimeSeconds = 0L,
                totalBreaksTaken = 0,
                totalBreakTimeSeconds = 0L
            )
        }
    }

    fun restartPomodoroPhase() {
        _uiState.update { 
            val baseTime = when (it.currentPhase) {
                PomodoroPhase.FOCUS -> it.baseFocusDurationMinutes
                PomodoroPhase.BREAK -> it.baseBreakDurationMinutes
                PomodoroPhase.LONG_BREAK -> it.longBreakDurationMinutes
            }
            it.copy(
                isPomodoroRunning = true,
                pomodoroTimeRemainingSeconds = baseTime * 60L,
                sessionExtraTimeSeconds = 0L
            )
        }
    }


    fun revertLiveExtraTime() {
        _uiState.update { state ->
            val newRemaining = (state.pomodoroTimeRemainingSeconds - state.sessionExtraTimeSeconds).coerceAtLeast(0L)
            state.copy(
                pomodoroTimeRemainingSeconds = newRemaining,
                sessionExtraTimeSeconds = 0L
            )
        }
    }

    fun addLiveExtraTime(seconds: Long) {
        _uiState.update { state ->
            val maxAllowed = if (state.currentPhase == PomodoroPhase.FOCUS) 360L * 60L else 120L * 60L
            val minAllowed = if (state.currentPhase == PomodoroPhase.FOCUS) 60L else 0L
            val newRemaining = (state.pomodoroTimeRemainingSeconds + seconds).coerceIn(minAllowed, maxAllowed)
            val actualDiff = newRemaining - state.pomodoroTimeRemainingSeconds
            state.copy(
                pomodoroTimeRemainingSeconds = newRemaining,
                sessionExtraTimeSeconds = state.sessionExtraTimeSeconds + actualDiff,
                liveAdjustmentCount = state.liveAdjustmentCount + 1
            )
        }
    }

    fun skipPomodoroPhase() {
        handlePomodoroPhaseComplete(isSkipped = true)
    }

    
    private fun playPomodoroAlert() {
        val app = getApplication<Application>()
        if (appSettings.pomodoroPhaseAlerts) {
            try {
                val toneGen = ToneGenerator(AudioManager.STREAM_NOTIFICATION, 100)
                toneGen.startTone(ToneGenerator.TONE_PROP_BEEP, 500)
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
        if (appSettings.pomodoroPhaseVibrationEnabled) {
            vibrate(app)
        }
    }

    
    private fun getBitmapFromVectorDrawable(context: Context, drawableId: Int): Bitmap {
        val drawable = ContextCompat.getDrawable(context, drawableId) ?: return Bitmap.createBitmap(1, 1, Bitmap.Config.ARGB_8888)
        val bitmap = Bitmap.createBitmap(
            drawable.intrinsicWidth,
            drawable.intrinsicHeight,
            Bitmap.Config.ARGB_8888
        )
        val canvas = Canvas(bitmap)
        drawable.setBounds(0, 0, canvas.width, canvas.height)
        drawable.draw(canvas)
        return bitmap
    }

    private fun vibrate(context: Context) {
        try {
            val vibrator = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                val vibratorManager = context.getSystemService(Context.VIBRATOR_MANAGER_SERVICE) as VibratorManager
                vibratorManager.defaultVibrator
            } else {
                @Suppress("DEPRECATION")
                context.getSystemService(Context.VIBRATOR_SERVICE) as Vibrator
            }

            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                vibrator.vibrate(VibrationEffect.createOneShot(500, VibrationEffect.DEFAULT_AMPLITUDE))
            } else {
                @Suppress("DEPRECATION")
                vibrator.vibrate(500)
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private fun handlePomodoroPhaseComplete(isSkipped: Boolean = false) {
        val state = _uiState.value
        
        var completedSessions = state.totalSessionsCompleted
        var currentSessionCount = state.currentSessionCount
        var breaksTaken = state.totalBreaksTaken
        
        val nextPhase: PomodoroPhase
        val nextBaseTime: Int
        
        if (state.currentPhase == PomodoroPhase.FOCUS) {
            if (!isSkipped) {
                completedSessions++
                currentSessionCount++
                appSettings.totalSessionsCompleted = completedSessions
                
                // Record stat
                viewModelScope.launch {
                    statsDao.insertStat(FocusSessionStats(
                        durationSeconds = state.baseFocusDurationMinutes * 60L,
                        isFocus = true,
                        type = "POMODORO"
                    ))
                }
            }
            
            if (currentSessionCount >= state.pomodoroTargetSessions && currentSessionCount > 0) {
                nextPhase = PomodoroPhase.LONG_BREAK
                nextBaseTime = state.longBreakDurationMinutes
                currentSessionCount = 0 // Reset cycle
            } else {
                nextPhase = PomodoroPhase.BREAK
                nextBaseTime = state.baseBreakDurationMinutes
            }
        } else {
            if (!isSkipped) {
                breaksTaken++
                appSettings.totalBreaksTaken = breaksTaken
                
                // Record stat
                viewModelScope.launch {
                    statsDao.insertStat(FocusSessionStats(
                        durationSeconds = if (state.currentPhase == PomodoroPhase.LONG_BREAK) state.longBreakDurationMinutes * 60L else state.baseBreakDurationMinutes * 60L,
                        isFocus = false,
                        type = "POMODORO_BREAK"
                    ))
                }
            }
            nextPhase = PomodoroPhase.FOCUS
            nextBaseTime = state.baseFocusDurationMinutes
        }
        
        playPomodoroAlert()
        _uiState.update { it.copy(
            isPomodoroRunning = true,
            currentPhase = nextPhase,
            pomodoroTimeRemainingSeconds = nextBaseTime * 60L,
            sessionExtraTimeSeconds = 0L,
            totalSessionsCompleted = completedSessions,
            currentSessionCount = currentSessionCount,
            totalBreaksTaken = breaksTaken
        ) }
    }

    fun setAppearanceMode(mode: Int) {
        appSettings.appearanceMode = mode
        _uiState.update { it.copy(appearanceMode = mode) }
    }

    // Theme
    fun setTheme(theme: String) {
        appSettings.currentTheme = theme
        _uiState.update { it.copy(currentTheme = theme) }
        if (theme != "Custom") {
            resetCustomColorsForThemeChange()
        }
    }
    
    fun setCustomColors(backdrop: String, baseText: String, overdueText: String) {
        appSettings.customBackdropColor = backdrop
        appSettings.customBaseTextColor = baseText
        appSettings.customOverdueTextColor = overdueText
        appSettings.currentTheme = "Custom"
        _uiState.update { it.copy(
            customBackdropColor = backdrop,
            customBaseTextColor = baseText,
            customOverdueTextColor = overdueText,
            currentTheme = "Custom"
        )}
    }
    
    private fun resetCustomColorsForThemeChange() {
        appSettings.customBackdropColor = ""
        appSettings.customBaseTextColor = ""
        appSettings.customOverdueTextColor = ""
        _uiState.update { it.copy(
            customBackdropColor = "",
            customBaseTextColor = "",
            customOverdueTextColor = ""
        )}
    }
    
    fun resetCustomColors() {
        setCustomColors("", "", "")
    }

    fun exportData(): String {
        val tasks = activeTasks.value + completedTasks.value
        val moshi = com.squareup.moshi.Moshi.Builder()
            .add(com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory())
            .build()
        val type = com.squareup.moshi.Types.newParameterizedType(List::class.java, TimerTask::class.java)
        val adapter: com.squareup.moshi.JsonAdapter<List<TimerTask>> = moshi.adapter(type)
        return adapter.toJson(tasks)
    }

    fun importData(json: String) {
        try {
            val moshi = com.squareup.moshi.Moshi.Builder()
                .add(com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory())
                .build()
            val type = com.squareup.moshi.Types.newParameterizedType(List::class.java, TimerTask::class.java)
            val adapter: com.squareup.moshi.JsonAdapter<List<TimerTask>> = moshi.adapter(type)
            val tasks = adapter.fromJson(json)
            tasks?.forEach { task ->
                viewModelScope.launch {
                    repository.insertTask(task)
                }
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    fun updateDailyFocusGoalMinutes(minutes: Int) {
        appSettings.dailyFocusGoalMinutes = minutes
        _uiState.update { it.copy(dailyFocusGoalMinutes = minutes) }
    }


    fun addCustomColor(hex: String) {
        val current = appSettings.customColors.toMutableSet()
        if (current.add(hex)) {
            appSettings.customColors = current
            _uiState.update { it.copy(customColors = current) }
        }
    }
    fun removeCustomColor(hex: String) {
        val current = appSettings.customColors.toMutableSet()
        if (current.remove(hex)) {
            appSettings.customColors = current
            _uiState.update { it.copy(customColors = current) }
        }
    }
    // Profile & Tags
    fun updateProfile(name: String, bio: String, imageUri: String) {
        appSettings.profileName = name
        appSettings.profileBio = bio
        appSettings.profileImageUri = imageUri
        _uiState.update { it.copy(profileName = name, profileBio = bio, profileImageUri = imageUri) }
    }

    fun addProfileCustomField(key: String, value: String) {
        val currentFields = _uiState.value.profileCustomFields.toMutableMap()
        currentFields[key] = value
        appSettings.profileCustomFields = currentFields.map { "${it.key}|${it.value}" }.toSet()
        _uiState.update { it.copy(profileCustomFields = currentFields) }
    }

    fun removeProfileCustomField(key: String) {
        val currentFields = _uiState.value.profileCustomFields.toMutableMap()
        currentFields.remove(key)
        appSettings.profileCustomFields = currentFields.map { "${it.key}|${it.value}" }.toSet()
        _uiState.update { it.copy(profileCustomFields = currentFields) }
    }

    fun updateProfileCustomField(oldKey: String, newKey: String, newValue: String) {
        val currentFields = _uiState.value.profileCustomFields.toMutableMap()
        if (oldKey != newKey) currentFields.remove(oldKey)
        currentFields[newKey] = newValue
        appSettings.profileCustomFields = currentFields.map { "${it.key}|${it.value}" }.toSet()
        _uiState.update { it.copy(profileCustomFields = currentFields) }
    }


    fun addCustomLabel(label: String) {
        val currentLabels = appSettings.customLabels.toMutableSet()
        if (!currentLabels.any { it.split("|").first() == label.split("|").first() }) {
            currentLabels.add(label)
            appSettings.customLabels = currentLabels
            _uiState.update { it.copy(customLabels = currentLabels) }
        }
    }

    fun removeCustomLabel(label: String) {
        val currentLabels = appSettings.customLabels.toMutableSet()
        if (currentLabels.remove(label)) {
            appSettings.customLabels = currentLabels
            _uiState.update { it.copy(customLabels = currentLabels) }





        }
    }

    fun deleteAccount() {
        appSettings.profileName = "Guest"
        appSettings.profileBio = ""
        appSettings.profileImageUri = ""
        appSettings.profileCustomFields = emptySet()
        appSettings.customLabels = emptySet()
        _uiState.update { it.copy(profileName = "Guest", profileBio = "", profileImageUri = "", profileCustomFields = emptyMap(), customLabels = emptySet()) }
    }

    fun factoryResetUserData() {
        viewModelScope.launch {
            // Delete all chronometers (TimerTasks)
            repository.deleteAllTasks()
            
            // Delete all stats
            statsDao.deleteAllStats()
            
            // Reset Pomodoro stats
            hardResetPomodoro()
            
            // Reset Profile
            deleteAccount()
            
            // Reset Custom Tags to default
            val defaultTags = setOf("Work", "Personal", "Health", "Study")
            appSettings.customLabels = defaultTags
            
            // Update UI State for profile and labels
            _uiState.update {
                it.copy(
                    customLabels = defaultTags
                )
            }
        }
    }

    // Settings toggles
    fun togglePreventHidingAllUnits(enabled: Boolean) {
        appSettings.preventHidingAllUnits = enabled
        _uiState.update { it.copy(preventHidingAllUnits = enabled) }
    }
    
    fun toggleColoredLabelsEnabled(enabled: Boolean) {
        appSettings.coloredLabelsEnabled = enabled
        _uiState.update { it.copy(coloredLabelsEnabled = enabled) }
    }

    
    fun togglePomodoroPhaseAlerts(enabled: Boolean) {
        appSettings.pomodoroPhaseAlerts = enabled
        _uiState.update { it.copy(pomodoroPhaseAlerts = enabled) }

    }

    
    fun toggleChronometerDeadlinesAlerts(enabled: Boolean) {
        appSettings.chronometerDeadlinesAlerts = enabled
        _uiState.update { it.copy(chronometerDeadlinesAlerts = enabled) }

    }

    
    fun togglePomodoroPhaseVibration(enabled: Boolean) {
        appSettings.pomodoroPhaseVibrationEnabled = enabled
        _uiState.update { it.copy(pomodoroPhaseVibrationEnabled = enabled) }
    }

    fun toggleChronometerDeadlineVibration(enabled: Boolean) {
        appSettings.chronometerDeadlineVibrationEnabled = enabled
        _uiState.update { it.copy(chronometerDeadlineVibrationEnabled = enabled) }
    }

    fun setChronometerDeadlineOffsetMinutes(minutes: Int) {
        appSettings.chronometerDeadlineOffsetMinutes = minutes
        _uiState.update { it.copy(chronometerDeadlineOffsetMinutes = minutes) }
    }

    

    fun togglePrivateJournalLock(enabled: Boolean) {
        appSettings.privateJournalLockEnabled = enabled
        _uiState.update { it.copy(privateJournalLockEnabled = enabled) }
    }

    fun toggleAppPasswordEnabled(enabled: Boolean) {
        appSettings.appPasswordEnabled = enabled
        _uiState.update { it.copy(appPasswordEnabled = enabled) }

    }

    
    fun setAppPassword(password: String) {
        appSettings.appPassword = password
        _uiState.update { it.copy(appPassword = password) }
    }

    fun setPasswordHint(hint: String) {
        appSettings.passwordHint = hint
        _uiState.update { it.copy(passwordHint = hint) }
    }
    
    fun setSecurityQuestionsAndAnswers(q1: String, a1: String, q2: String, a2: String, q3: String, a3: String) {
        appSettings.securityQuestion = q1
        appSettings.securityAnswer = a1
        appSettings.securityQuestion2 = q2
        appSettings.securityAnswer2 = a2
        appSettings.securityQuestion3 = q3
        appSettings.securityAnswer3 = a3
        _uiState.update { it.copy(
            securityQuestion = q1, securityAnswer = a1,
            securityQuestion2 = q2, securityAnswer2 = a2,
            securityQuestion3 = q3, securityAnswer3 = a3
        ) }
    }

    
    fun toggleBiometricsEnabled(enabled: Boolean) {
        appSettings.biometricsEnabled = enabled
        _uiState.update { it.copy(biometricsEnabled = enabled) }

    }

    
        fun lockApp() {
        if (appSettings.appPasswordEnabled || appSettings.biometricsEnabled) {
            _uiState.update { it.copy(isAuthenticated = false) }
        }
    }

    fun setAuthenticated(auth: Boolean) {
        _uiState.update { it.copy(isAuthenticated = auth) }

    }

    
    fun clearHistory() {
        viewModelScope.launch {
            repository.deleteAllCompletedTasks()
        }

    }


    fun setPomodoroFullscreenTheme(theme: String) {
        appSettings.pomodoroFullscreenTheme = theme
        _uiState.update { it.copy(pomodoroFullscreenTheme = theme) }
    }

    fun adjustPomodoroTime(seconds: Long) {
        _uiState.update { state ->
            val newTime = (state.pomodoroTimeRemainingSeconds + seconds).coerceAtLeast(0L)
            state.copy(
                pomodoroTimeRemainingSeconds = newTime,
                liveAdjustmentCount = state.liveAdjustmentCount + 1
            )
        }
    }

    // Daily Schedule Operations

        fun deleteDailyScheduleSync(id: String, deleteEntireSeries: Boolean = false) {
        viewModelScope.launch(kotlinx.coroutines.Dispatchers.IO) {
            val db = com.example.data.AppDatabase.getDatabase(getApplication())
            val existing = db.dailyScheduleDao().getScheduleSync(id)
            if (existing != null) {
                if (deleteEntireSeries && existing.seriesId != null) {
                    db.dailyScheduleDao().deleteSeries(existing.seriesId)
                } else {
                    db.dailyScheduleDao().deleteSchedule(existing)
                }
                recalculateAllLanes(db)
            }
        }
    }

fun updateDailyScheduleDraft(draft: com.example.data.DailyScheduleDraft) {
        _uiState.update { it.copy(dailyScheduleDraft = draft) }
    }
    
    fun clearDailyScheduleDraft() {
        _uiState.update { it.copy(dailyScheduleDraft = com.example.data.DailyScheduleDraft(label = "")) }
    }
    
    fun saveAdvancedDailySchedule(draft: com.example.data.DailyScheduleDraft, editEntireSeries: Boolean = false) {
        viewModelScope.launch(kotlinx.coroutines.Dispatchers.IO) {
            val db = com.example.data.AppDatabase.getDatabase(getApplication())
            val duration = draft.endTime - draft.startTime
            
            // Delete old if editing
            var targetSeriesId = draft.seriesId
            if (draft.editingId != null) {
                val existing = db.dailyScheduleDao().getScheduleSync(draft.editingId)
                if (existing != null) {
                    if (editEntireSeries && existing.seriesId != null) {
                        val timeDelta = draft.startTime - existing.startTime
                        db.dailyScheduleDao().updateSeries(existing.seriesId, draft.title, draft.label, timeDelta)
                        recalculateAllLanes(db)
                        clearDailyScheduleDraft()
                        return@launch
                    } else {
                        if (targetSeriesId != null) {
                            db.dailyScheduleDao().breakFromSeries(draft.editingId)
                            targetSeriesId = null
                        }
                        db.dailyScheduleDao().deleteSchedule(existing)
                    }
                }
            }
            
            if (!draft.isRecurring) {
                db.dailyScheduleDao().insertSchedule(
                    com.example.data.DailyScheduleTask(
                        id = draft.editingId ?: java.util.UUID.randomUUID().toString(),
                        title = draft.title,
                        startTime = draft.startTime,
                        endTime = draft.endTime,
                        label = draft.label,
                        seriesId = targetSeriesId
                    )
                )
            } else {
                if (targetSeriesId == null) { targetSeriesId = java.util.UUID.randomUUID().toString() }
                val maxDays = appSettings.recurrenceGenerationCapYears * 365
                
                val pattern = draft.toRecurrencePattern()
                val occurrences = pattern.generateOccurrences(draft.startTime, maxIterations = maxDays)
                
                occurrences.forEachIndexed { index, currentStart ->
                    val currentEnd = currentStart + duration
                    val taskId = if (index == 0 && draft.editingId != null) draft.editingId else java.util.UUID.randomUUID().toString()
                    
                    db.dailyScheduleDao().insertSchedule(
                        com.example.data.DailyScheduleTask(
                            id = taskId,
                            title = draft.title,
                            startTime = currentStart,
                            endTime = currentEnd,
                            label = draft.label,
                            seriesId = targetSeriesId,
                            recurrenceType = draft.recurrenceType.name
                        )
                    )
                }
            }
            recalculateAllLanes(db)
        }
        clearDailyScheduleDraft()
    }

    
    private fun getVisualBounds(task: com.example.data.DailyScheduleTask): Pair<Long, Long> {
        val durationMillis = task.endTime - task.startTime
        val durationMinutes = durationMillis / 60000L
        val endCal = java.util.Calendar.getInstance().apply { timeInMillis = task.endTime }
        val endMinutes = endCal.get(java.util.Calendar.HOUR_OF_DAY) * 60 + endCal.get(java.util.Calendar.MINUTE)
        
        val titleLen = task.title.length
        val tagLen = task.label.length
        val maxTextLen = maxOf(titleLen.toFloat(), tagLen.toFloat() * 0.8f)
        // Adjust estimated width: 44dp base + 8dp per title char + 28dp for status icon
        val estimatedWidthDp = 44 + 28 + (maxTextLen * 8)
        val visualMinutes = estimatedWidthDp / 1.5f
        val visualDurationMillis = (visualMinutes * 60 * 1000L).toLong()
        
        val alignTextEnd = durationMinutes < 150 && endMinutes > 22 * 60
        
        if (alignTextEnd) {
            val visualStart = task.endTime - maxOf(durationMillis, visualDurationMillis)
            return Pair(minOf(task.startTime, visualStart), task.endTime)
        } else {
            val visualEnd = task.startTime + maxOf(durationMillis, visualDurationMillis)
            return Pair(task.startTime, maxOf(task.endTime, visualEnd))
        }
    }

    private suspend fun recalculateAllLanes(db: com.example.data.AppDatabase, exemptTaskId: String? = null) {
        val tasks = db.dailyScheduleDao().getAllSchedulesSync()
        
        val activeTasks = tasks.filter { !it.isFinished }.sortedBy { it.startTime }
        val finishedTasks = tasks.filter { it.isFinished }.sortedBy { it.startTime }
        
        val updatedTasks = mutableListOf<com.example.data.DailyScheduleTask>()
        
        // Active Tasks Float
        val activeLaneEnds = mutableMapOf<Int, Long>()
        for (task in activeTasks) {
            val visualBounds = getVisualBounds(task)
            var lane = if (task.id == exemptTaskId) task.laneIndex else 0
            while (true) {
                val laneEnd = activeLaneEnds[lane] ?: 0L
                if (visualBounds.first >= laneEnd) {
                    activeLaneEnds[lane] = visualBounds.second
                    updatedTasks.add(task.copy(laneIndex = lane))
                    break
                }
                lane++
            }
        }
        
        val maxActiveLane = if (activeLaneEnds.isEmpty()) -1 else activeLaneEnds.keys.maxOrNull() ?: -1
        
        // Completion Drop
        val finishedLaneEnds = mutableMapOf<Int, Long>()
        for (task in finishedTasks) {
            val visualBounds = getVisualBounds(task)
            var lane = maxActiveLane + 1
            while (true) {
                val laneEnd = finishedLaneEnds[lane] ?: 0L
                if (visualBounds.first >= laneEnd) {
                    finishedLaneEnds[lane] = visualBounds.second
                    updatedTasks.add(task.copy(laneIndex = lane))
                    break
                }
                lane++
            }
        }
        
        // Update all tasks in db
        db.dailyScheduleDao().updateSchedules(updatedTasks)
    }

    fun addDailySchedule(title: String, startTime: Long, endTime: Long, label: String, recurringDays: Set<Int> = emptySet()) {
        viewModelScope.launch(Dispatchers.IO) {
            val db = com.example.data.AppDatabase.getDatabase(getApplication())
            if (recurringDays.isEmpty()) {
                db.dailyScheduleDao().insertSchedule(
                    DailyScheduleTask(title = title, startTime = startTime, endTime = endTime, label = label)
                )
                recalculateAllLanes(db)
            } else {
                val duration = endTime - startTime
                val cal = java.util.Calendar.getInstance().apply { timeInMillis = startTime }
                
                // Generate for the next 4 weeks (28 days)
                for (i in 0 until 28) {
                    val dayOfWeek = cal.get(java.util.Calendar.DAY_OF_WEEK)
                    if (recurringDays.contains(dayOfWeek)) {
                        val currentStart = cal.timeInMillis
                        val currentEnd = currentStart + duration
                        db.dailyScheduleDao().insertSchedule(
                            DailyScheduleTask(title = title, startTime = currentStart, endTime = currentEnd, label = label)
                        )
                    }
                    cal.add(java.util.Calendar.DAY_OF_YEAR, 1)
                }
                recalculateAllLanes(db)
            }
        }
    }

    fun updateDailySchedule(schedule: DailyScheduleTask) {
        viewModelScope.launch(Dispatchers.IO) {
            val db = com.example.data.AppDatabase.getDatabase(getApplication())
            db.dailyScheduleDao().updateSchedule(schedule)
            recalculateAllLanes(db, exemptTaskId = schedule.id)
        }
    }

        fun deleteDailySchedule(schedule: DailyScheduleTask, deleteEntireSeries: Boolean = false) {
        viewModelScope.launch(kotlinx.coroutines.Dispatchers.IO) {
            val db = com.example.data.AppDatabase.getDatabase(getApplication())
            if (deleteEntireSeries && schedule.seriesId != null) {
                db.dailyScheduleDao().deleteSeries(schedule.seriesId)
            } else {
                db.dailyScheduleDao().deleteSchedule(schedule)
            }
            recalculateAllLanes(db)
        }
    }
    
fun insertJournalEntry(entry: com.example.data.JournalEntry) {
        viewModelScope.launch(Dispatchers.IO) {
            journalDao.insertEntry(entry)
        }
    }

    fun updateJournalEntry(entry: com.example.data.JournalEntry) {
        viewModelScope.launch(Dispatchers.IO) {
            journalDao.updateEntry(entry)
        }
    }

    fun deleteJournalEntry(entry: com.example.data.JournalEntry) {
        viewModelScope.launch(Dispatchers.IO) {
            journalDao.deleteEntry(entry)
        }
    }
    fun insertJournalTemplate(template: com.example.data.JournalTemplate) {
        viewModelScope.launch(Dispatchers.IO) {
            journalDao.insertTemplate(template)
        }
    }

    fun updateJournalTemplate(template: com.example.data.JournalTemplate) {
        viewModelScope.launch(Dispatchers.IO) {
            journalDao.updateTemplate(template)
        }
    }

    fun deleteJournalTemplate(template: com.example.data.JournalTemplate) {
        viewModelScope.launch(Dispatchers.IO) {
            journalDao.deleteTemplate(template)
        }
    }
    
    private val gson = Gson()

    
    fun setUse24HourFormat(use24Hour: Boolean) {
        appSettings.use24HourFormat = use24Hour
        _uiState.update { it.copy(use24HourFormat = use24Hour) }
    }
        
    fun setEnableDailyScheduleRadioMenu(enabled: Boolean) {
        appSettings.enableDailyScheduleRadioMenu = enabled
        _uiState.update { it.copy(enableDailyScheduleRadioMenu = enabled) }
    }
    
    fun setAutoStatusIfMissed(status: String) {
        appSettings.autoStatusIfMissed = status
        _uiState.update { it.copy(autoStatusIfMissed = status) }
    }
}
