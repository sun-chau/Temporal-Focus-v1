with open("app/src/main/java/com/example/ui/screens/UserAccountScreen.kt", "r") as f:
    content = f.read()

chip_border_old = """border = BorderStroke(2.dp, if (tagColorValue != Color.Transparent) tagColorValue else MaterialTheme.colorScheme.outline),"""
chip_border_new = """border = BorderStroke(1.dp, if (tagColorValue != Color.Transparent) outlineColor else MaterialTheme.colorScheme.outline),"""
content = content.replace(chip_border_old, chip_border_new)

cat_border_old = """border = BorderStroke(2.dp, if (categoryColorValue != Color.Transparent) categoryColorValue else MaterialTheme.colorScheme.outline),"""
cat_border_new = """border = BorderStroke(1.dp, if (categoryColorValue != Color.Transparent) outlineColor else MaterialTheme.colorScheme.outline),"""
content = content.replace(cat_border_old, cat_border_new)

with open("app/src/main/java/com/example/ui/screens/UserAccountScreen.kt", "w") as f:
    f.write(content)
