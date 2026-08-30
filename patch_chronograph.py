import re

with open('app/src/main/java/com/example/ui/screens/LandscapeChronographScreen.kt', 'r') as f:
    content = f.read()

# 1. Add Build import
if "import android.os.Build" not in content:
    content = content.replace("import android.os.BatteryManager", "import android.os.BatteryManager\nimport android.os.Build")

# 2. Add Display Cutout Mode logic
target_window_setup = """        activity?.window?.let { window ->
            androidx.core.view.WindowInsetsControllerCompat(window, window.decorView).apply {
                hide(androidx.core.view.WindowInsetsCompat.Type.systemBars())
                systemBarsBehavior = androidx.core.view.WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
            }
        }"""
        
replacement_window_setup = """        activity?.window?.let { window ->
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
                window.attributes = window.attributes.apply {
                    layoutInDisplayCutoutMode = WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES
                }
            }
            androidx.core.view.WindowInsetsControllerCompat(window, window.decorView).apply {
                hide(androidx.core.view.WindowInsetsCompat.Type.systemBars())
                systemBarsBehavior = androidx.core.view.WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
            }
        }"""
        
content = content.replace(target_window_setup, replacement_window_setup)

# 3. Add Safe Drawing Insets to Box
target_box = """    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(backgroundColor)
            .padding(16.dp)
    ) {"""

replacement_box = """    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(backgroundColor)
            .windowInsetsPadding(WindowInsets.safeDrawing)
            .padding(16.dp)
    ) {"""

content = content.replace(target_box, replacement_box)

with open('app/src/main/java/com/example/ui/screens/LandscapeChronographScreen.kt', 'w') as f:
    f.write(content)
