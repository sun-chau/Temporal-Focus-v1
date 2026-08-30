with open("app/src/main/java/com/example/ui/screens/UserAccountScreen.kt", "r") as f:
    content = f.read()

content = content.replace("onClick = { tagColor = allAvailableColors.randomOrNull() ?: \\"#9E9E9E\\" }", "onTap = { _ -> tagColor = allAvailableColors.randomOrNull() ?: \\"#9E9E9E\\" }")
content = content.replace("onClick = { categoryColor = allAvailableColors.randomOrNull() ?: \\"#9E9E9E\\" }", "onTap = { _ -> categoryColor = allAvailableColors.randomOrNull() ?: \\"#9E9E9E\\" }")

with open("app/src/main/java/com/example/ui/screens/UserAccountScreen.kt", "w") as f:
    f.write(content)
