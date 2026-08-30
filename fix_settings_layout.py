import re

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

# We need to make sure the in app notification is fully functioning with the coming soon toast properly placed.
# Everything is well formed.
