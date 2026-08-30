import re

with open('app/src/main/java/com/example/ui/components/QuickReminderSheet.kt', 'r') as f:
    content = f.read()

# Remove windowInsets = WindowInsets.ime from ModalBottomSheet
# and add .windowInsetsPadding(WindowInsets.ime) to the Row modifier.
old_modal = """    ModalBottomSheet(
        onDismissRequest = onDismiss,
        windowInsets = WindowInsets.ime
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(start = 16.dp, end = 16.dp, bottom = 24.dp),"""

new_modal = """    ModalBottomSheet(
        onDismissRequest = onDismiss
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .windowInsetsPadding(WindowInsets.ime)
                .padding(start = 16.dp, end = 16.dp, bottom = 24.dp),"""

if old_modal in content:
    content = content.replace(old_modal, new_modal)
else:
    print("Warning: Could not find old_modal pattern")

with open('app/src/main/java/com/example/ui/components/QuickReminderSheet.kt', 'w') as f:
    f.write(content)

