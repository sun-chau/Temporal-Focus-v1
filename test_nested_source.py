import os

content = """
import androidx.compose.ui.input.nestedscroll.NestedScrollSource

fun main() {
    println(NestedScrollSource.Drag.toString())
    println(NestedScrollSource.UserInput.toString())
}
"""
with open("app/src/main/java/com/example/ui/screens/TestNestedSource.kt", "w") as f:
    f.write(content)

