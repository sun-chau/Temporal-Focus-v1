import os

content = """
import androidx.compose.ui.input.nestedscroll.NestedScrollSource

fun main() {
    val source = NestedScrollSource.Drag
    val isDrag = source == NestedScrollSource.UserInput || source == NestedScrollSource.Drag
    println("isDrag: " + isDrag)
}
"""
with open("app/src/main/java/com/example/ui/screens/TestNestedSource2.kt", "w") as f:
    f.write(content)

