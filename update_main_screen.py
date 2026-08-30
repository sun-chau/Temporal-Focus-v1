import re

with open("app/src/main/java/com/example/ui/screens/MainScreen.kt", "r") as f:
    content = f.read()

# 1. Update font size of "Hi Guest"
content = content.replace("fontSize = 24.sp,", "fontSize = 28.sp,")

# 2. Update GlobalHeader padding and icon
search_global = r'''    val formattedDate = formatter\.format\(date\)
    
    Row\(
        modifier = Modifier
            \.fillMaxWidth\(\)
            \.clip\(RoundedCornerShape\(12\.dp\)\)
            \.background\(MaterialTheme\.colorScheme\.surface\)
            \.padding\(16\.dp\),
        verticalAlignment = Alignment\.CenterVertically,
        horizontalArrangement = Arrangement\.Center
    \) \{
        Icon\(
            imageVector = Icons\.Default\.Schedule,
            contentDescription = "Clock",'''

replace_global = '''    val formattedDate = formatter.format(date)
    
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(12.dp))
            .background(MaterialTheme.colorScheme.surface)
            .padding(vertical = 8.dp, horizontal = 16.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.Center
    ) {
        Icon(
            imageVector = androidx.compose.ui.graphics.vector.ImageVector.vectorResource(id = com.example.R.drawable.ic_nested_clock_farsight_analog),
            contentDescription = "Clock",'''

content = re.sub(search_global, replace_global, content)

if "import androidx.compose.ui.res.vectorResource" not in content:
    content = content.replace("import androidx.compose.ui.unit.sp", "import androidx.compose.ui.unit.sp\nimport androidx.compose.ui.res.vectorResource")

with open("app/src/main/java/com/example/ui/screens/MainScreen.kt", "w") as f:
    f.write(content)
