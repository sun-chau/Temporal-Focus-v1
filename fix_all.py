import re

with open("app/src/main/java/com/example/ui/screens/BurnRateTrackerUI.kt", "r") as f:
    content = f.read()

# Add component at the end
component = """
@Composable
fun ScrollToLatestButton(
    visible: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    androidx.compose.animation.AnimatedVisibility(
        visible = visible,
        modifier = modifier
    ) {
        Box(
            modifier = Modifier
                .size(48.dp)
                .background(MaterialTheme.colorScheme.surfaceVariant, RectangleShape)
                .border(2.dp, MaterialTheme.colorScheme.outline, RectangleShape)
                .clickable { onClick() },
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = Icons.Default.KeyboardArrowDown,
                contentDescription = "Jump to Latest",
                tint = MaterialTheme.colorScheme.onSurface
            )
        }
    }
}
"""
if "fun ScrollToLatestButton" not in content:
    content = content + component

# Replace AnimatedVisibility usage
old_usage = """        AnimatedVisibility(
            visible = showScrollToLatest,
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .padding(16.dp)
        ) {
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .background(MaterialTheme.colorScheme.surfaceVariant, RectangleShape)
                    .border(2.dp, MaterialTheme.colorScheme.outline, RectangleShape)
                    .clickable {
                        coroutineScope.launch {
                            listState.animateScrollToItem(0)
                        }
                    },
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Default.KeyboardArrowDown,
                    contentDescription = "Jump to Latest",
                    tint = MaterialTheme.colorScheme.onSurface
                )
            }
        }"""

new_usage = """        ScrollToLatestButton(
            visible = showScrollToLatest,
            onClick = { coroutineScope.launch { listState.animateScrollToItem(0) } },
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .padding(16.dp)
        )
        } // ends Box"""

content = content.replace(old_usage, new_usage)

with open("app/src/main/java/com/example/ui/screens/BurnRateTrackerUI.kt", "w") as f:
    f.write(content)

