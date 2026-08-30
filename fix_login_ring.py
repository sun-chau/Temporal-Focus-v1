import re

with open("app/src/main/java/com/example/ui/screens/LoginScreen.kt", "r") as f:
    content = f.read()

box_old = r'''            Box\(
                modifier = Modifier
                    \.size\(120\.dp\)
                    \.clip\(CircleShape\)
                    \.background\(MaterialTheme\.colorScheme\.surfaceVariant\),
                contentAlignment = Alignment\.Center
            \) \{
                if \(uiState\.profileImageUri\.isNotEmpty\(\)\) \{
                    AsyncImage\(
                        model = ImageRequest\.Builder\(LocalContext\.current\)
                            \.data\(uiState\.profileImageUri\)
                            \.crossfade\(true\)
                            \.build\(\),
                        contentDescription = "Profile Picture",
                        contentScale = ContentScale\.Crop,
                        modifier = Modifier\.fillMaxSize\(\)
                    \)'''

box_new = '''            Box(
                modifier = Modifier
                    .size(128.dp)
                    .border(2.dp, MaterialTheme.colorScheme.primary, CircleShape)
                    .padding(6.dp),
                contentAlignment = Alignment.Center
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .clip(CircleShape)
                        .background(MaterialTheme.colorScheme.surfaceVariant),
                    contentAlignment = Alignment.Center
                ) {
                    if (uiState.profileImageUri.isNotEmpty()) {
                        AsyncImage(
                            model = ImageRequest.Builder(LocalContext.current)
                                .data(uiState.profileImageUri)
                                .crossfade(true)
                                .build(),
                            contentDescription = "Profile Picture",
                            contentScale = ContentScale.Crop,
                            modifier = Modifier.fillMaxSize()
                        )'''

content = re.sub(box_old, box_new, content)

# ensure border is imported
if "import androidx.compose.foundation.border" not in content:
    content = content.replace("import androidx.compose.foundation.background", "import androidx.compose.foundation.background\nimport androidx.compose.foundation.border")

with open("app/src/main/java/com/example/ui/screens/LoginScreen.kt", "w") as f:
    f.write(content)
