import re

with open('app/src/main/java/com/example/ui/screens/MainScreen.kt', 'r') as f:
    content = f.read()

old_block = """                        }
                    }
                }
            }
        }
    }
}

@Composable"""

new_block = """                        }
                    }
                }
            }
        }

        if (uiState.showQuickReminderSheet) {
            com.example.ui.components.QuickReminderSheet(
                onDismiss = { viewModel.setQuickReminderSheet(false) },
                onSave = { name, time -> viewModel.addQuickReminder(name, time) }
            )
        }
    }
}

@Composable"""

if old_block in content:
    content = content.replace(old_block, new_block)

with open('app/src/main/java/com/example/ui/screens/MainScreen.kt', 'w') as f:
    f.write(content)

