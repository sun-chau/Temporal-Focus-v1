package com.example.data

import android.content.Context
import android.content.SharedPreferences

class AppSettings(context: Context) {
    var launcherIcon: String
        get() = prefs.getString("launcher_icon", "orange") ?: "orange"
        set(value) = prefs.edit().putString("launcher_icon", value).apply()

    private val prefs: SharedPreferences = context.getSharedPreferences(
        "app_settings",
        Context.MODE_PRIVATE
    )

    var selectedDisplayIds: String
        get() = prefs.getString("selected_display_ids", "") ?: ""
        set(value) = prefs.edit().putString("selected_display_ids", value).apply()
        
    var maxStageSlots: Int
        get() = prefs.getInt("max_stage_slots", 5)
        set(value) = prefs.edit().putInt("max_stage_slots", value).apply()
        
    var isUrgentMode: Boolean
        get() = prefs.getBoolean("is_urgent_mode", false)
        set(value) = prefs.edit().putBoolean("is_urgent_mode", value).apply()

    var layoutPreference: String // "vertical" or "horizontal"
        get() = prefs.getString("layout_pref", "vertical") ?: "vertical"
        set(value) = prefs.edit().putString("layout_pref", value).apply()
        
    var showYears: Boolean
        get() = prefs.getBoolean("show_years", true)
        set(value) = prefs.edit().putBoolean("show_years", value).apply()
        
    var showMonths: Boolean
        get() = prefs.getBoolean("show_months", true)
        set(value) = prefs.edit().putBoolean("show_months", value).apply()
        
    var showDays: Boolean
        get() = prefs.getBoolean("show_days", true)
        set(value) = prefs.edit().putBoolean("show_days", value).apply()

    var showHours: Boolean
        get() = prefs.getBoolean("show_hours", true)
        set(value) = prefs.edit().putBoolean("show_hours", value).apply()
        
    var showMinutes: Boolean
        get() = prefs.getBoolean("show_minutes", true)
        set(value) = prefs.edit().putBoolean("show_minutes", value).apply()

    var showSeconds: Boolean
        get() = prefs.getBoolean("show_seconds", true)
        set(value) = prefs.edit().putBoolean("show_seconds", value).apply()


    // Themes (Midnight, Amber, Nordic)
    var appearanceMode: Int // 0=System, 1=Light, 2=Dark
        get() = prefs.getInt("appearance_mode", 0)
        set(value) = prefs.edit().putInt("appearance_mode", value).apply()

    var currentTheme: String
        get() = prefs.getString("current_theme", "Default") ?: "Default"
        set(value) = prefs.edit().putString("current_theme", value).apply()
        
    var pomodoroFullscreenTheme: String
        get() = prefs.getString("pomodoro_fullscreen_theme", "Default Light") ?: "Default Light"
        set(value) = prefs.edit().putString("pomodoro_fullscreen_theme", value).apply()
        
    var customBackdropColor: String
        get() = prefs.getString("custom_backdrop", "") ?: ""
        set(value) = prefs.edit().putString("custom_backdrop", value).apply()
        
    var customBaseTextColor: String
        get() = prefs.getString("custom_base_text", "") ?: ""
        set(value) = prefs.edit().putString("custom_base_text", value).apply()
        
    var customOverdueTextColor: String
        get() = prefs.getString("custom_overdue_text", "") ?: ""
        set(value) = prefs.edit().putString("custom_overdue_text", value).apply()

        
    // Pomodoro Stats & Settings
    var baseFocusDurationMinutes: Int
        get() = prefs.getInt("pomodoro_focus_min", 25)
        set(value) = prefs.edit().putInt("pomodoro_focus_min", value).apply()
        
    var baseBreakDurationMinutes: Int
        get() = prefs.getInt("pomodoro_break_min", 5)
        set(value) = prefs.edit().putInt("pomodoro_break_min", value).apply()
        
    var totalSessionsCompleted: Int
        get() = prefs.getInt("pomodoro_sessions", 0)
        set(value) = prefs.edit().putInt("pomodoro_sessions", value).apply()
        
    var totalFocusTimeSeconds: Long
        get() = prefs.getLong("pomodoro_total_seconds", 0L)
        set(value) = prefs.edit().putLong("pomodoro_total_seconds", value).apply()

    var totalBreakTimeSeconds: Long
        get() = prefs.getLong("pomodoro_total_break_seconds", 0L)
        set(value) = prefs.edit().putLong("pomodoro_total_break_seconds", value).apply()

    var totalBreaksTaken: Int
        get() = prefs.getInt("pomodoro_breaks_taken", 0)
        set(value) = prefs.edit().putInt("pomodoro_breaks_taken", value).apply()

    var pomodoroTargetSessions: Int
        get() = prefs.getInt("pomodoro_target_sessions", 4)
        set(value) = prefs.edit().putInt("pomodoro_target_sessions", value).apply()

    var longBreakDurationMinutes: Int
        get() = prefs.getInt("pomodoro_long_break_min", 15)
        set(value) = prefs.edit().putInt("pomodoro_long_break_min", value).apply()
    // Profile Settings
    var profileName: String
        get() = prefs.getString("profile_name", "Guest") ?: "Guest"
        set(value) = prefs.edit().putString("profile_name", value).apply()

    var profileBio: String
        get() = prefs.getString("profile_bio", "") ?: ""
        set(value) = prefs.edit().putString("profile_bio", value).apply()

    var profileImageUri: String
        get() = prefs.getString("profile_image_uri", "") ?: ""
        set(value) = prefs.edit().putString("profile_image_uri", value).apply()
        
    var profileCustomFields: Set<String>
        get() = prefs.getStringSet("profile_custom_fields", emptySet()) ?: emptySet()
        set(value) = prefs.edit().putStringSet("profile_custom_fields", value).apply()

    var customColors: Set<String>
        get() = prefs.getStringSet("custom_colors", emptySet()) ?: emptySet()
        set(value) = prefs.edit().putStringSet("custom_colors", value).apply()
    var customLabels: Set<String>
        get() = prefs.getStringSet("custom_labels", setOf("Work", "Personal", "Health", "Study", "Leisure", "Other")) ?: setOf("Work", "Personal", "Health", "Study", "Leisure", "Other")
        set(value) = prefs.edit().putStringSet("custom_labels", value).apply()



    var dailyFocusGoalMinutes: Int
        get() = prefs.getInt("daily_focus_goal_minutes", 0)
        set(value) = prefs.edit().putInt("daily_focus_goal_minutes", value).apply()

    // Display


    var coloredLabelsEnabled: Boolean
        get() = prefs.getBoolean("colored_labels_enabled", true)
        set(value) = prefs.edit().putBoolean("colored_labels_enabled", value).apply()



    var preventHidingAllUnits: Boolean
        get() = prefs.getBoolean("prevent_hiding_all", true)
        set(value) = prefs.edit().putBoolean("prevent_hiding_all", value).apply()

    // Notifications
    var pomodoroPhaseAlerts: Boolean
        get() = prefs.getBoolean("pomodoro_phase_alerts", true)
        set(value) = prefs.edit().putBoolean("pomodoro_phase_alerts", value).apply()
        
    var pomodoroPhaseVibrationEnabled: Boolean
        get() = prefs.getBoolean("pomodoro_phase_vibration", true)
        set(value) = prefs.edit().putBoolean("pomodoro_phase_vibration", value).apply()

    var chronometerDeadlinesAlerts: Boolean
        get() = prefs.getBoolean("chronometer_deadlines_alerts", true)
        set(value) = prefs.edit().putBoolean("chronometer_deadlines_alerts", value).apply()
        
    var chronometerDeadlineVibrationEnabled: Boolean
        get() = prefs.getBoolean("chronometer_deadline_vibration", true)
        set(value) = prefs.edit().putBoolean("chronometer_deadline_vibration", value).apply()
        
    var chronometerDeadlineOffsetMinutes: Int
        get() = prefs.getInt("chronometer_deadline_offset", 0)
        set(value) = prefs.edit().putInt("chronometer_deadline_offset", value).apply()

    

    

    // Security
    var privateJournalLockEnabled: Boolean
        get() = prefs.getBoolean("private_journal_lock_enabled", true)
        set(value) = prefs.edit().putBoolean("private_journal_lock_enabled", value).apply()

    var appPasswordEnabled: Boolean
        get() = prefs.getBoolean("app_password_enabled", false)
        set(value) = prefs.edit().putBoolean("app_password_enabled", value).apply()

    var appPassword: String
        get() = prefs.getString("app_password", "") ?: ""
        set(value) = prefs.edit().putString("app_password", value).apply()

    var passwordHint: String
        get() = prefs.getString("password_hint", "") ?: ""
        set(value) = prefs.edit().putString("password_hint", value).apply()
        
    var securityQuestion: String
        get() = prefs.getString("security_question", "") ?: ""
        set(value) = prefs.edit().putString("security_question", value).apply()
        
    var securityAnswer: String
        get() = prefs.getString("security_answer", "") ?: ""
        set(value) = prefs.edit().putString("security_answer", value).apply()
        
    var securityQuestion2: String
        get() = prefs.getString("security_question2", "") ?: ""
        set(value) = prefs.edit().putString("security_question2", value).apply()
        
    var securityAnswer2: String
        get() = prefs.getString("security_answer2", "") ?: ""
        set(value) = prefs.edit().putString("security_answer2", value).apply()
        
    var securityQuestion3: String
        get() = prefs.getString("security_question3", "") ?: ""
        set(value) = prefs.edit().putString("security_question3", value).apply()
        
    var securityAnswer3: String
        get() = prefs.getString("security_answer3", "") ?: ""
        set(value) = prefs.edit().putString("security_answer3", value).apply()

    var biometricsEnabled: Boolean
        get() = prefs.getBoolean("biometrics_enabled", false)
        set(value) = prefs.edit().putBoolean("biometrics_enabled", value).apply()

    // Daily Schedule Settings
    var use24HourFormat: Boolean
        get() = prefs.getBoolean("use_24_hour_format", true)
        set(value) = prefs.edit().putBoolean("use_24_hour_format", value).apply()
        
    var recurrenceGenerationCapYears: Int
        get() = prefs.getInt("recurrence_generation_cap_years", 1)
        set(value) = prefs.edit().putInt("recurrence_generation_cap_years", value).apply()
        
        var enableDailyScheduleRadioMenu: Boolean
        get() = prefs.getBoolean("enable_daily_schedule_radio_menu", true)
        set(value) = prefs.edit().putBoolean("enable_daily_schedule_radio_menu", value).apply()

    var autoStatusIfMissed: String
        get() = prefs.getString("auto_status_missed", "NOT_DONE") ?: "NOT_DONE"
        set(value) = prefs.edit().putString("auto_status_missed", value).apply()

}
