import re

with open("app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt", "r") as f:
    content = f.read()

# We need ManageTimersScreen to end properly:
search_str = r'''                \} else \{
                    CompletedHistoryTab\(
                        tasks = completedTasks,
                        onDelete = \{ viewModel\.deleteTask\(it\) \}
                    \)
                \}
            \}
        \}
\}
@Composable'''

replace_str = '''                } else {
                    CompletedHistoryTab(
                        tasks = completedTasks,
                        onDelete = { viewModel.deleteTask(it) }
                    )
                }
            }
        }
    }
}

@Composable'''

content = re.sub(search_str, replace_str, content)

with open("app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt", "w") as f:
    f.write(content)
