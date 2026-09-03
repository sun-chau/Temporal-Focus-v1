import re

with open('app/src/main/java/com/example/ui/screens/CheckInsScreen.kt', 'r') as f:
    content = f.read()

# Add a state variable for selectedTracker
if 'var selectedTracker by remember' not in content:
    content = content.replace(
        'var showSheet by remember { mutableStateOf(false) }',
        'var showSheet by remember { mutableStateOf(false) }\n    var selectedTracker by remember { mutableStateOf<TrackerEntity?>(null) }'
    )

# Replace the Toast click handler
toast_code = 'Toast.makeText(context, "Payload UI Rendering: COMING SOON", Toast.LENGTH_SHORT).show()'
if toast_code in content:
    content = content.replace(toast_code, 'selectedTracker = tracker')

# Wrap everything in an if-else for selectedTracker
if 'if (selectedTracker != null)' not in content:
    content = content.replace(
        'Scaffold(',
        'if (selectedTracker != null) {\n        TrackerDetailRouter(\n            tracker = selectedTracker!!,\n            viewModel = viewModel,\n            onBack = { selectedTracker = null }\n        )\n    } else {\n    Scaffold('
    )
    
    # We need to find the end of the Scaffold and close the else block.
    # The Scaffold block is roughly closed before `if (showSheet)`
    # This might be tricky with regex, let's just do a manual string replace.
    # The function ends at:
    #     if (showSheet) {
    #         NewTrackerSheet(
    #             onDismiss = { showSheet = false },
    #             ...
    #         )
    #     }
    # }
    
    content = content.replace(
"""    if (showSheet) {
        NewTrackerSheet(
            onDismiss = { showSheet = false },
            onSave = { title, type ->
                viewModel.insertTracker(
                    TrackerEntity(
                        title = title,
                        type = type,
                        payloadData = "{}"
                    )
                )
                showSheet = false
            }
        )
    }
}""",
"""    if (showSheet) {
        NewTrackerSheet(
            onDismiss = { showSheet = false },
            onSave = { title, type ->
                viewModel.insertTracker(
                    TrackerEntity(
                        title = title,
                        type = type,
                        payloadData = "{}"
                    )
                )
                showSheet = false
            }
        )
    }
    }
}"""
    )


with open('app/src/main/java/com/example/ui/screens/CheckInsScreen.kt', 'w') as f:
    f.write(content)

