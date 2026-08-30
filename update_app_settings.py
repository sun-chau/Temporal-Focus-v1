path = 'app/src/main/java/com/example/data/AppSettings.kt'
with open(path, 'r') as f:
    content = f.read()

settings_fields = """
    // Display
    var preventHidingAllUnits: Boolean
        get() = prefs.getBoolean("prevent_hiding_all", true)
        set(value) = prefs.edit().putBoolean("prevent_hiding_all", value).apply()

    // Notifications
    var pomodoroPhaseAlerts: Boolean
        get() = prefs.getBoolean("pomodoro_phase_alerts", true)
        set(value) = prefs.edit().putBoolean("pomodoro_phase_alerts", value).apply()

    var chronometerDeadlinesAlerts: Boolean
        get() = prefs.getBoolean("chronometer_deadlines_alerts", true)
        set(value) = prefs.edit().putBoolean("chronometer_deadlines_alerts", value).apply()

    var alertSoundEnabled: Boolean
        get() = prefs.getBoolean("alert_sound_enabled", true)
        set(value) = prefs.edit().putBoolean("alert_sound_enabled", value).apply()

    var alertVibrationEnabled: Boolean
        get() = prefs.getBoolean("alert_vibration_enabled", true)
        set(value) = prefs.edit().putBoolean("alert_vibration_enabled", value).apply()

    // Security
    var appPasswordEnabled: Boolean
        get() = prefs.getBoolean("app_password_enabled", false)
        set(value) = prefs.edit().putBoolean("app_password_enabled", value).apply()

    var appPassword: String
        get() = prefs.getString("app_password", "") ?: ""
        set(value) = prefs.edit().putString("app_password", value).apply()

    var biometricsEnabled: Boolean
        get() = prefs.getBoolean("biometrics_enabled", false)
        set(value) = prefs.edit().putBoolean("biometrics_enabled", value).apply()
}"""

content = content.replace("}", settings_fields)

with open(path, 'w') as f:
    f.write(content)
