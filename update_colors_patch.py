import re

# AppSettings.kt
with open("app/src/main/java/com/example/data/AppSettings.kt", "r") as f:
    content = f.read()

colors_prop = """    var customColors: Set<String>
        get() = prefs.getStringSet("custom_colors", emptySet()) ?: emptySet()
        set(value) = prefs.edit().putStringSet("custom_colors", value).apply()
"""
if "customColors: Set<String>" not in content:
    content = content.replace("    var customTags: Set<String>", colors_prop + "    var customTags: Set<String>")
    with open("app/src/main/java/com/example/data/AppSettings.kt", "w") as f:
        f.write(content)

# MainViewModel.kt
with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

ui_state_add = "    val customColors: Set<String> = emptySet(),\n"
if "val customColors: Set<String> =" not in content:
    content = content.replace("    val customCategories: Set<String> = setOf(", ui_state_add + "    val customCategories: Set<String> = setOf(")

load_colors = "            customColors = appSettings.customColors,\n"
if "customColors = appSettings.customColors," not in content:
    content = content.replace("            customCategories = appSettings.customCategories,", load_colors + "            customCategories = appSettings.customCategories,")

functions = """
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
"""
if "fun addCustomColor" not in content:
    content = content.replace("    // Profile & Tags", functions + "    // Profile & Tags")

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)

