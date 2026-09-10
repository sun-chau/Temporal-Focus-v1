import re

with open("app/src/main/java/com/example/ui/screens/AssignmentTrackerUI.kt", "r") as f:
    content = f.read()

old_sig = """fun TerminalWheelPicker(
    items: List<String>,
    onItemSelected: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    val listState = rememberLazyListState()"""

new_sig = """fun TerminalWheelPicker(
    items: List<String>,
    onItemSelected: (String) -> Unit,
    modifier: Modifier = Modifier,
    initialSelection: String? = null
) {
    val initialIndex = initialSelection?.let { items.indexOf(it).takeIf { idx -> idx >= 0 } } ?: 0
    val listState = rememberLazyListState(initialFirstVisibleItemIndex = initialIndex)"""

content = content.replace(old_sig, new_sig)

with open("app/src/main/java/com/example/ui/screens/AssignmentTrackerUI.kt", "w") as f:
    f.write(content)
