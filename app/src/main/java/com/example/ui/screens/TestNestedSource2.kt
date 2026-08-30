
import androidx.compose.ui.input.nestedscroll.NestedScrollSource

fun main() {
    val source = NestedScrollSource.Drag
    val isDrag = source == NestedScrollSource.UserInput || source == NestedScrollSource.Drag
    println("isDrag: " + isDrag)
}
