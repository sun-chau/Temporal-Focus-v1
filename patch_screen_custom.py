import re

with open('app/src/main/java/com/example/ui/screens/TrackerDetailScreen.kt', 'r') as f:
    content = f.read()

imports_to_add = """
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.ui.text.input.KeyboardType
"""
if 'import androidx.compose.foundation.text.KeyboardOptions' not in content:
    content = content.replace('import androidx.compose.ui.unit.sp', 'import androidx.compose.ui.unit.sp\n' + imports_to_add)

router_replacement = """            when (tracker.type) {
                TrackerType.CUSTOM -> {
                    if (payload is CustomPayload) {
                        CustomTrackerUI(tracker, payload, viewModel)
                    } else {
                        Text("Invalid Custom Payload", color = MaterialTheme.colorScheme.error)
                    }
                }
                TrackerType.GYM -> {"""

if 'TrackerType.CUSTOM -> {' not in content:
    content = content.replace('            when (tracker.type) {\n                TrackerType.GYM -> {', router_replacement)

with open('app/src/main/java/com/example/ui/screens/TrackerDetailScreen.kt', 'w') as f:
    f.write(content)
