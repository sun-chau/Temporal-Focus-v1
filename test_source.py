import os

content = """
import androidx.compose.ui.input.nestedscroll.NestedScrollSource

fun check() {
    val a = NestedScrollSource.Drag
    val b = NestedScrollSource.Fling
}
"""
with open("app/src/main/java/com/example/ui/screens/TestSource.kt", "w") as f:
    f.write(content)

