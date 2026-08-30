import re

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "r") as f:
    content = f.read()

# Make FilterList and ViewCarousel boxes to be identical to TouchApp box
# Replace IconButton with Box
# FilterList
content = re.sub(
r'''IconButton\(
                        onClick = \{ showStageFilterDialog = true \},
                        modifier = Modifier
                            \.size\(36\.dp\)
                            \.clip\(RoundedCornerShape\(8\.dp\)\)
                            \.background\(Color\(0xFF1E1E1E\)\)
                            \.border\(1\.dp, Color\.White\.copy\(alpha = 0\.1f\), RoundedCornerShape\(8\.dp\)\)
                    \) \{
                        Icon\(Icons\.Default\.FilterList, contentDescription = "Filter Stage", tint = Color\.White, modifier = Modifier\.size\(20\.dp\)\)
                    \}''',
r'''Box(
                        modifier = Modifier
                            .size(36.dp)
                            .clip(RoundedCornerShape(8.dp))
                            .background(Color(0xFF1E1E1E))
                            .border(1.dp, Color.White.copy(alpha = 0.1f), RoundedCornerShape(8.dp))
                            .clickable { showStageFilterDialog = true },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(Icons.Default.FilterList, contentDescription = "Filter Stage", tint = Color.White, modifier = Modifier.size(20.dp))
                    }''', content)

# Layout Toggle
content = re.sub(
r'''IconButton\(
                        onClick = \{
                            if \(isVertical\) \{
                                viewModel\.setLayoutPreference\(ChronometerLayout\.HORIZONTAL\)
                            \} else \{
                                viewModel\.setLayoutPreference\(ChronometerLayout\.VERTICAL\)
                            \}
                        \},
                        modifier = Modifier
                            \.size\(36\.dp\)
                            \.clip\(RoundedCornerShape\(8\.dp\)\)
                            \.background\(Color\(0xFF1E1E1E\)\)
                            \.border\(1\.dp, Color\.White\.copy\(alpha = 0\.1f\), RoundedCornerShape\(8\.dp\)\)
                    \) \{
                        Icon\(
                            if \(isVertical\) Icons\.Default\.ViewCarousel else Icons\.Default\.ViewAgenda,
                            contentDescription = "Toggle Layout",
                            tint = Color\.White,
                            modifier = Modifier\.size\(20\.dp\)
                        \)
                    \}''',
r'''Box(
                        modifier = Modifier
                            .size(36.dp)
                            .clip(RoundedCornerShape(8.dp))
                            .background(Color(0xFF1E1E1E))
                            .border(1.dp, Color.White.copy(alpha = 0.1f), RoundedCornerShape(8.dp))
                            .clickable {
                                if (isVertical) {
                                    viewModel.setLayoutPreference(ChronometerLayout.HORIZONTAL)
                                } else {
                                    viewModel.setLayoutPreference(ChronometerLayout.VERTICAL)
                                }
                            },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            if (isVertical) Icons.Default.ViewCarousel else Icons.Default.ViewAgenda,
                            contentDescription = "Toggle Layout",
                            tint = Color.White,
                            modifier = Modifier.size(20.dp)
                        )
                    }''', content)

# Update Add Icon size
content = content.replace('Icon(Icons.Default.Add, contentDescription = "Create", tint = MaterialTheme.colorScheme.background, modifier = Modifier.size(32.dp))', 'Icon(Icons.Default.Add, contentDescription = "Create", tint = MaterialTheme.colorScheme.background, modifier = Modifier.size(40.dp))')

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "w") as f:
    f.write(content)
