import re

with open("app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt", "r") as f:
    content = f.read()

old_on_value_change = """                        onValueChange = { newValue ->
                            var finalValue = newValue
                            if (newValue.text != textValue.text) {
                                // check for new line to preserve indentation
                                if (newValue.text.length > textValue.text.length) {
                                    val newChars = newValue.text.substring(textValue.text.length)
                                    if (newChars == "\n") {
                                        // find previous line indentation
                                        val lines = textValue.text.split("\\n")
                                        val lastLine = lines.lastOrNull() ?: ""
                                        val indent = lastLine.takeWhile { it == ' ' || it == '\\t' }
                                        if (indent.isNotEmpty()) {
                                            val before = newValue.text.substring(0, newValue.selection.start)
                                            val after = newValue.text.substring(newValue.selection.start)
                                            finalValue = TextFieldValue(
                                                text = before + indent + after,
                                                selection = TextRange(newValue.selection.start + indent.length)
                                            )
                                        }
                                    }
                                }
                            }
                            textValue = finalValue
                            isDirty = true
                        },"""

new_on_value_change = """                        onValueChange = { newValue ->
                            var finalValue = newValue
                            if (newValue.text != textValue.text) {
                                // check if exactly one newline was inserted at the cursor
                                if (newValue.text.length - textValue.text.length == 1 && 
                                    newValue.selection.start > 0 && 
                                    newValue.text[newValue.selection.start - 1] == '\\n') {
                                    
                                    val beforeCursor = newValue.text.substring(0, newValue.selection.start - 1)
                                    val lastLine = beforeCursor.substringAfterLast('\\n')
                                    val indent = lastLine.takeWhile { it == ' ' || it == '\\t' }
                                    
                                    if (indent.isNotEmpty()) {
                                        val before = newValue.text.substring(0, newValue.selection.start)
                                        val after = newValue.text.substring(newValue.selection.start)
                                        finalValue = TextFieldValue(
                                            text = before + indent + after,
                                            selection = TextRange(newValue.selection.start + indent.length)
                                        )
                                    }
                                }
                            }
                            textValue = finalValue
                            isDirty = true
                        },"""

if old_on_value_change in content:
    content = content.replace(old_on_value_change, new_on_value_change)
    print("Successfully patched onValueChange")
else:
    print("Could not find old_on_value_change")

with open("app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt", "w") as f:
    f.write(content)
