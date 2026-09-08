import re

with open("app/src/main/java/com/example/ui/screens/BurnRateTrackerUI.kt", "r") as f:
    content = f.read()

# 2. Add State variables
state_old = """    var tagToDelete by remember { mutableStateOf<String?>(null) }

    val tags = listOf("GENERAL", "FOOD", "TRANSPORT") + payload.customTags.toList()"""
state_new = """    var tagToDelete by remember { mutableStateOf<String?>(null) }
    val listState = rememberLazyListState()
    val coroutineScope = rememberCoroutineScope()
    val showScrollToLatest by remember { derivedStateOf { listState.firstVisibleItemIndex > 2 } }

    val tags = listOf("GENERAL", "FOOD", "TRANSPORT") + payload.customTags.toList()"""
content = content.replace(state_old, state_new)

with open("app/src/main/java/com/example/ui/screens/BurnRateTrackerUI.kt", "w") as f:
    f.write(content)

