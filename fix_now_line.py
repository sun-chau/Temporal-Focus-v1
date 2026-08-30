import re
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

content = content.replace("modifier = modifier.shadow(elevation, shape, clip = false)\n            .offset(x = xOffset)", "modifier = modifier\n            .offset(x = xOffset)")

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
