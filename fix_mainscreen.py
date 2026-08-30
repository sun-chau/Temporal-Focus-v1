import re

with open('app/src/main/java/com/example/ui/screens/MainScreen.kt', 'r') as f:
    content = f.read()

# I want to add QuickDeadlineSheet at the very end of MainScreen composable
old_end = """        }
    }
}

@Composable
fun GlobalHeader"""

new_end = """        }
    }
    
    if (uiState.showQuickDeadlineSheet) {
        com.example.ui.components.QuickDeadlineSheet(viewModel = viewModel, uiState = uiState)
    }
}

@Composable
fun GlobalHeader"""

content = content.replace(old_end, new_end)

with open('app/src/main/java/com/example/ui/screens/MainScreen.kt', 'w') as f:
    f.write(content)
