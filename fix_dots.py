import re

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "r") as f:
    content = f.read()

vertical_old = r'''                if \(uiState\.layoutPreference == ChronometerLayout\.VERTICAL\) \{
                    LazyColumn\(modifier = Modifier\.weight\(1f\)\) \{
                        items\(displayTasks\) \{ task ->
                            ChronometerItem\(task, uiState\.currentDateTime, viewModel\)
                            Spacer\(modifier = Modifier\.height\(16\.dp\)\)
                        \}
                        
                        item \{
                            Spacer\(modifier = Modifier\.height\(64\.dp\)\) // padding for fab
                        \}
                    \}
                \}'''

vertical_new = '''                if (uiState.layoutPreference == ChronometerLayout.VERTICAL) {
                    val listState = rememberLazyListState()
                    val firstVisibleIndex by remember { derivedStateOf { listState.firstVisibleItemIndex } }
                    Row(modifier = Modifier.weight(1f)) {
                        LazyColumn(state = listState, modifier = Modifier.weight(1f)) {
                            items(displayTasks) { task ->
                                ChronometerItem(task, uiState.currentDateTime, viewModel)
                                Spacer(modifier = Modifier.height(16.dp))
                            }
                            
                            item {
                                Spacer(modifier = Modifier.height(64.dp)) // padding for fab
                            }
                        }
                        
                        if (displayTasks.size > 1) {
                            Spacer(modifier = Modifier.width(8.dp))
                            Column(
                                modifier = Modifier.fillMaxHeight().padding(bottom = 64.dp),
                                verticalArrangement = Arrangement.Center,
                                horizontalAlignment = Alignment.CenterHorizontally
                            ) {
                                if (displayTasks.size >= 50) {
                                    val progress = if (displayTasks.isEmpty()) 0f else firstVisibleIndex.toFloat() / displayTasks.size
                                    Box(modifier = Modifier.width(4.dp).height(200.dp).background(Color.DarkGray, RoundedCornerShape(2.dp))) {
                                        Box(
                                            modifier = Modifier
                                                .fillMaxWidth()
                                                .height((200f * (1f / displayTasks.size)).coerceAtLeast(10f).dp)
                                                .offset(y = (progress * 200).dp)
                                                .background(MaterialTheme.colorScheme.primary, RoundedCornerShape(2.dp))
                                        )
                                    }
                                } else {
                                    displayTasks.forEachIndexed { index, _ ->
                                        val isSelected = index == firstVisibleIndex
                                        val height = if (isSelected) 16.dp else 6.dp
                                        val color = if (isSelected) MaterialTheme.colorScheme.primary else Color.DarkGray
                                        Box(
                                            modifier = Modifier
                                                .padding(vertical = 2.dp)
                                                .width(6.dp)
                                                .height(height)
                                                .clip(RoundedCornerShape(3.dp))
                                                .background(color)
                                        )
                                    }
                                }
                            }
                        }
                    }
                }'''

content = re.sub(vertical_old, vertical_new, content)

# Check for lazy list state import
if "import androidx.compose.foundation.lazy.rememberLazyListState" not in content:
    content = content.replace("import androidx.compose.foundation.lazy.LazyColumn", "import androidx.compose.foundation.lazy.LazyColumn\nimport androidx.compose.foundation.lazy.rememberLazyListState")

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "w") as f:
    f.write(content)

