with open("app/src/main/java/com/example/ui/screens/TrackerDetailRouter.kt", "r") as f:
    content = f.read()

old_else = """                else -> {
                    Text("Payload UI Rendering: COMING SOON", fontFamily = FontFamily.Monospace)
                }
            }
        }
    }
}"""

new_else = """                TrackerType.BINARY -> {
                    if (payload is BinaryPayload) {
                        BinaryTrackerUI(tracker, payload, viewModel)
                    } else {
                        Text("Invalid Binary Payload", color = MaterialTheme.colorScheme.error)
                    }
                }
                TrackerType.VOLUME -> {
                    if (payload is VolumePayload) {
                        VolumeTrackerUI(tracker, payload, viewModel)
                    } else {
                        Text("Invalid Volume Payload", color = MaterialTheme.colorScheme.error)
                    }
                }
                TrackerType.BURN_RATE -> {
                    if (payload is BurnRatePayload) {
                        BurnRateTrackerUI(tracker, payload, viewModel)
                    } else {
                        Text("Invalid BurnRate Payload", color = MaterialTheme.colorScheme.error)
                    }
                }
            }
        }
    }
}"""
content = content.replace(old_else, new_else)

with open("app/src/main/java/com/example/ui/screens/TrackerDetailRouter.kt", "w") as f:
    f.write(content)
