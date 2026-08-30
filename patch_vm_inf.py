import re

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

search = "val limit = draft.occurrenceCount.coerceAtLeast(1)"
replace = "val limit = if (draft.occurrenceCount <= 0) Int.MAX_VALUE else draft.occurrenceCount"
content = content.replace(search, replace)

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
