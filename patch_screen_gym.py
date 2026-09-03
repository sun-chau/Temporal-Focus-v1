import re

with open('app/src/main/java/com/example/ui/screens/TrackerDetailScreen.kt', 'r') as f:
    content = f.read()

imports_to_add = """
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.UUID
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.ui.unit.sp
"""
if 'import java.util.Date' not in content:
    content = content.replace('import com.example.viewmodel.MainViewModel', 'import com.example.viewmodel.MainViewModel\n' + imports_to_add)

router_replacement = """            when (tracker.type) {
                TrackerType.GYM -> {
                    if (payload is GymPayload) {
                        GymTrackerUI(tracker, payload, viewModel)
                    } else {
                        Text("Invalid Gym Payload", color = MaterialTheme.colorScheme.error)
                    }
                }
                TrackerType.SYLLABUS -> {"""

if 'TrackerType.GYM -> {' not in content:
    content = content.replace('            when (tracker.type) {\n                TrackerType.SYLLABUS -> {', router_replacement)

with open('app/src/main/java/com/example/ui/screens/TrackerDetailScreen.kt', 'w') as f:
    f.write(content)
