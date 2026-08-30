import androidx.compose.ui.input.nestedscroll.NestedScrollSource

fun test(s: NestedScrollSource) {
    if (s == NestedScrollSource.Drag) {
        println("Drag exists")
    }
}
