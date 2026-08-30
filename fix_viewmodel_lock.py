import re

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

lock_app = """    fun lockApp() {
        if (appSettings.appPasswordEnabled || appSettings.biometricsEnabled) {
            _uiState.update { it.copy(isAuthenticated = false) }
        }
    }"""

if "fun lockApp" not in content:
    content = content.replace("fun authenticate", lock_app + "\n\n    fun authenticate")

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
