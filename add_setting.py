import re

# AppSettings.kt
with open("app/src/main/java/com/example/data/AppSettings.kt", "r") as f:
    app_settings = f.read()

new_setting = """    var enableDailyScheduleRadioMenu: Boolean
        get() = prefs.getBoolean("enable_daily_schedule_radio_menu", true)
        set(value) = prefs.edit().putBoolean("enable_daily_schedule_radio_menu", value).apply()
"""
app_settings = app_settings.replace("var autoStatusIfMissed: String", new_setting + "\n    var autoStatusIfMissed: String")

with open("app/src/main/java/com/example/data/AppSettings.kt", "w") as f:
    f.write(app_settings)

# UiState in MainViewModel.kt
with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    view_model = f.read()

# 1. add to UiState
view_model = view_model.replace(
    "val autoStatusIfMissed: String = \"NOT_DONE\",",
    "val autoStatusIfMissed: String = \"NOT_DONE\",\n    val enableDailyScheduleRadioMenu: Boolean = true,"
)

# 2. populate in init
view_model = view_model.replace(
    "autoStatusIfMissed = appSettings.autoStatusIfMissed,",
    "autoStatusIfMissed = appSettings.autoStatusIfMissed,\n            enableDailyScheduleRadioMenu = appSettings.enableDailyScheduleRadioMenu,"
)

# 3. add function
func = """
    fun setEnableDailyScheduleRadioMenu(enabled: Boolean) {
        appSettings.enableDailyScheduleRadioMenu = enabled
        _uiState.update { it.copy(enableDailyScheduleRadioMenu = enabled) }
    }
"""
view_model = view_model.replace("fun setAutoStatusIfMissed", func + "\n    fun setAutoStatusIfMissed")

# 4. update TimerMode enum
view_model = view_model.replace(
    "SETTINGS_FEATURE, SETTINGS_NOTIFICATIONS",
    "SETTINGS_FEATURE, SETTINGS_DAILY_SCHEDULE, SETTINGS_REMINDERS, SETTINGS_NOTIFICATIONS"
)

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(view_model)
