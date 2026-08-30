import os

path = 'app/src/main/java/com/example/data/AppSettings.kt'
with open(path, 'r') as f:
    content = f.read()

patch = """
    // Themes (Midnight, Amber, Nordic)
    var currentTheme: String
        get() = prefs.getString("current_theme", "Midnight Minimalist") ?: "Midnight Minimalist"
        set(value) = prefs.edit().putString("current_theme", value).apply()
        
    var customBackdropColor: String
        get() = prefs.getString("custom_backdrop", "") ?: ""
        set(value) = prefs.edit().putString("custom_backdrop", value).apply()
        
    var customBaseTextColor: String
        get() = prefs.getString("custom_base_text", "") ?: ""
        set(value) = prefs.edit().putString("custom_base_text", value).apply()
        
    var customOverdueTextColor: String
        get() = prefs.getString("custom_overdue_text", "") ?: ""
        set(value) = prefs.edit().putString("custom_overdue_text", value).apply()
"""

content = content.replace(
    """    // Themes (Midnight, Amber, Nordic)
    var currentTheme: String
        get() = prefs.getString("current_theme", "Midnight Minimalist") ?: "Midnight Minimalist"
        set(value) = prefs.edit().putString("current_theme", value).apply()""",
    patch
)

with open(path, 'w') as f:
    f.write(content)
