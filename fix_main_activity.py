import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

on_stop_method = """  override fun onStop() {
    super.onStop()
    viewModel.lockApp()
  }"""

if "override fun onStop" not in content:
    content = content.replace("  override fun onCreate(", on_stop_method + "\n\n  override fun onCreate(")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
