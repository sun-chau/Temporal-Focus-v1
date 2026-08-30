import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.input.nestedscroll.NestedScrollConnection
import androidx.compose.ui.input.nestedscroll.NestedScrollSource
import androidx.compose.ui.unit.Velocity

fun createNestedScrollConnection(
    onOverscroll: (Float) -> Unit
): NestedScrollConnection {
    return object : NestedScrollConnection {
        override fun onPostScroll(
            consumed: Offset,
            available: Offset,
            source: NestedScrollSource
        ): Offset {
            if (available.x != 0f) {
                onOverscroll(available.x)
            }
            return super.onPostScroll(consumed, available, source)
        }
    }
}
