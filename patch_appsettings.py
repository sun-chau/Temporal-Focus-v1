import sys

with open("app/src/main/java/com/example/data/AppSettings.kt", "r") as f:
    content = f.read()

new_fields = """
    // Daily Schedule Settings
    var use24HourFormat: Boolean
        get() = prefs.getBoolean("use_24_hour_format", true)
        set(value) = prefs.edit().putBoolean("use_24_hour_format", value).apply()
        
    var autoStatusIfMissed: String
        get() = prefs.getString("auto_status_missed", "NOT_DONE") ?: "NOT_DONE"
        set(value) = prefs.edit().putString("auto_status_missed", value).apply()
"""

# Insert before closing brace
last_brace_idx = content.rfind("}")
if last_brace_idx != -1:
    content = content[:last_brace_idx] + new_fields + "\n}" + content[last_brace_idx+1:]
else:
    print("Failed to find closing brace")
    sys.exit(1)

with open("app/src/main/java/com/example/data/AppSettings.kt", "w") as f:
    f.write(content)
