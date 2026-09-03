import re
with open("app/src/main/java/com/example/ui/screens/TrackerDetailRouter.kt", "r") as f:
    content = f.read()

new_router = """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TrackerDetailRouter(
    initialTracker: TrackerEntity,
    viewModel: TrackerViewModel,
    onBack: () -> Unit
) {
    val trackerState by viewModel.getTrackerById(initialTracker.id).collectAsState(initial = initialTracker)
    val tracker = trackerState ?: initialTracker
    val payload = viewModel.getParsedPayload(tracker)

    Scaffold(
"""

content = re.sub(
    r'@OptIn\(ExperimentalMaterial3Api::class\)\s*@Composable\s*fun TrackerDetailRouter\(\s*tracker: TrackerEntity,\s*viewModel: TrackerViewModel,\s*onBack: \(\) -> Unit\s*\)\s*\{\s*val payload = viewModel.getParsedPayload\(tracker\)\s*Scaffold\(',
    new_router,
    content
)

content = content.replace("tracker: TrackerEntity,", "initialTracker: TrackerEntity,") # just in case

with open("app/src/main/java/com/example/ui/screens/TrackerDetailRouter.kt", "w") as f:
    f.write(content)
