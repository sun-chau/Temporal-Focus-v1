import re

with open("app/src/main/java/com/example/ui/screens/MainScreen.kt", "r") as f:
    content = f.read()

# I will just ensure the version chip is on the next line.
chip_row_old = r'''                                Text\(
                                    text = "Temporal Focus",
                                    style = MaterialTheme\.typography\.titleLarge,
                                    fontWeight = FontWeight\.Bold,
                                    color = MaterialTheme\.colorScheme\.onSurface
                                \)
                                Spacer\(modifier = Modifier\.width\(8\.dp\)\)
                                Box\(
                                    modifier = Modifier
                                        \.border\(1\.dp, MaterialTheme\.colorScheme\.primary\.copy\(alpha = 0\.5f\), RoundedCornerShape\(50\)\)
                                        \.padding\(horizontal = 6\.dp, vertical = 2\.dp\)
                                \) \{
                                    Text\(
                                        text = "v\$\{updateLogs\.firstOrNull\(\)\?\.timestamp \?: com\.example\.BuildConfig\.VERSION_NAME\}",
                                        style = MaterialTheme\.typography\.labelSmall,
                                        color = MaterialTheme\.colorScheme\.primary,
                                        fontWeight = FontWeight\.Bold
                                    \)
                                \}'''

chip_row_new = '''                                Text(
                                    text = "Temporal Focus",
                                    style = MaterialTheme.typography.titleLarge,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.onSurface
                                )
                            }
                            Spacer(modifier = Modifier.height(4.dp))
                            Box(
                                modifier = Modifier
                                    .border(1.dp, MaterialTheme.colorScheme.primary.copy(alpha = 0.5f), RoundedCornerShape(50))
                                    .padding(horizontal = 6.dp, vertical = 2.dp)
                            ) {
                                Text(
                                    text = "v${updateLogs.firstOrNull()?.timestamp ?: com.example.BuildConfig.VERSION_NAME}",
                                    style = MaterialTheme.typography.labelSmall,
                                    color = MaterialTheme.colorScheme.primary,
                                    fontWeight = FontWeight.Bold
                                )
                            }'''

# Replace it.
# Note: Since chip_row_old matches the elements inside Row(verticalAlignment = Alignment.CenterVertically),
# The new block will close that Row after "Temporal Focus", and put the Box directly inside the Column.
content = re.sub(chip_row_old, chip_row_new, content)

with open("app/src/main/java/com/example/ui/screens/MainScreen.kt", "w") as f:
    f.write(content)
