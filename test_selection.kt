import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.TimePickerState

@OptIn(ExperimentalMaterial3Api::class)
fun checkSelection(state: TimePickerState) {
    val m = state.javaClass.methods.map { it.name }.joinToString(", ")
    println("METHODS: $m")
}
