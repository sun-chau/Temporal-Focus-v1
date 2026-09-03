import re
with open("app/src/main/java/com/example/ui/screens/TrackerDashboardScreen.kt", "r") as f:
    content = f.read()

new_block = """                            Text(
                                text = tracker.title,
                                fontWeight = FontWeight.Bold,
                                style = MaterialTheme.typography.titleLarge
                            )
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(
                                text = viewModel.getTelemetryString(tracker),
                                fontFamily = FontFamily.Monospace,
                                fontSize = androidx.compose.ui.unit.TextUnit(12f, androidx.compose.ui.unit.TextUnitType.Sp),
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )"""

content = content.replace("""                            Text(
                                text = tracker.title,
                                fontWeight = FontWeight.Bold,
                                style = MaterialTheme.typography.titleLarge
                            )""", new_block)

with open("app/src/main/java/com/example/ui/screens/TrackerDashboardScreen.kt", "w") as f:
    f.write(content)
