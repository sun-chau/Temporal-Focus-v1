import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.TimePickerState

@OptIn(ExperimentalMaterial3Api::class)
fun testState(state: TimePickerState) {
    // state.hour = 10 // Will this compile?
}
