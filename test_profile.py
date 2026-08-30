import re

with open('app/src/main/java/com/example/ui/screens/MainScreen.kt', 'r') as f:
    content = f.read()

if "profileImageUri" in content:
    print("Profile image is in MainScreen")
else:
    print("Profile image is MISSING in MainScreen")
