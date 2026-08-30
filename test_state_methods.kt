import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.TimePickerState

@OptIn(ExperimentalMaterial3Api::class)
fun checkState(state: TimePickerState) {
    // try to find setters
    val t: Any = state
    println(t.javaClass.methods.map { it.name })
}
