import re

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

lock_app = """    fun lockApp() {
        if (appSettings.appPasswordEnabled || appSettings.biometricsEnabled) {
            _uiState.update { it.copy(isAuthenticated = false) }
        }
    }"""

if "fun lockApp" not in content:
    content = content.replace("fun setAuthenticated", lock_app + "\n\n    fun setAuthenticated")

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
