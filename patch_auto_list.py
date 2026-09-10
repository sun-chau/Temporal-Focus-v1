import re

with open("app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt", "r") as f:
    content = f.read()

target = """                                        val match = Regex("^(\\\\s*[-*]\\\\s+|\\\\s*\\\\d+\\\\.\\\\s+)").find(prevLine)
                                        if (match != null) {
                                            val prefix = match.value
                                            val before = newValue.text.substring(0, newValue.selection.start)
                                            val after = newValue.text.substring(newValue.selection.start)
                                            finalValue = TextFieldValue(
                                                text = before + prefix + after,
                                                selection = TextRange(newValue.selection.start + prefix.length)
                                            )
                                        }"""

replacement = """                                        val match = Regex("^(\\\\s*[-*]\\\\s+|\\\\s*\\\\d+\\\\.\\\\s+)").find(prevLine)
                                        if (match != null) {
                                            if (match.value == prevLine) {
                                                // Empty list item: user pressed enter again. Remove the list prefix.
                                                val before = newValue.text.substring(0, prevLineStart)
                                                val after = newValue.text.substring(newValue.selection.start)
                                                finalValue = TextFieldValue(
                                                    text = before + "\\n" + after,
                                                    selection = TextRange(prevLineStart + 1)
                                                )
                                            } else {
                                                val prefix = match.value
                                                val before = newValue.text.substring(0, newValue.selection.start)
                                                val after = newValue.text.substring(newValue.selection.start)
                                                finalValue = TextFieldValue(
                                                    text = before + prefix + after,
                                                    selection = TextRange(newValue.selection.start + prefix.length)
                                                )
                                            }
                                        }"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt", "w") as f:
        f.write(content)
    print("Patched auto list")
else:
    print("Could not find auto list target")

