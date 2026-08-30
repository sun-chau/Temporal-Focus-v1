with open("app/src/main/java/com/example/ui/screens/LandscapeChronographScreen.kt", "r") as f:
    content = f.read()

content = content.replace(
    "context.registerReceiver(receiver, filter)",
    "androidx.core.content.ContextCompat.registerReceiver(context, receiver, filter, androidx.core.content.ContextCompat.RECEIVER_NOT_EXPORTED)"
)

with open("app/src/main/java/com/example/ui/screens/LandscapeChronographScreen.kt", "w") as f:
    f.write(content)
