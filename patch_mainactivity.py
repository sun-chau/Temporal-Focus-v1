import re
with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

old_code = """        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        enableEdgeToEdge()"""

new_code = """        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            window.attributes = window.attributes.apply {
                layoutInDisplayCutoutMode = WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES
            }
        }
        enableEdgeToEdge()"""

content = content.replace(old_code, new_code)
with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
