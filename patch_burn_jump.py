import re

with open("app/src/main/java/com/example/ui/screens/BurnRateTrackerUI.kt", "r") as f:
    content = f.read()

# 1. Add imports
imports = """
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.lazy.rememberLazyListState
import kotlinx.coroutines.launch
import androidx.compose.material.icons.filled.KeyboardArrowDown
"""
if "import androidx.compose.animation.AnimatedVisibility" not in content:
    content = content.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier" + imports)

# 2. Add State variables
state_old = """    var tagToDelete by remember { mutableStateOf<String?>(null) }
    val tags = listOf("GENERAL", "FOOD", "TRANSPORT") + payload.customTags.toList()"""
state_new = """    var tagToDelete by remember { mutableStateOf<String?>(null) }
    val listState = rememberLazyListState()
    val coroutineScope = rememberCoroutineScope()
    val showScrollToLatest by remember { derivedStateOf { listState.firstVisibleItemIndex > 2 } }
    val tags = listOf("GENERAL", "FOOD", "TRANSPORT") + payload.customTags.toList()"""
content = content.replace(state_old, state_new)

# 3. Modify LazyColumn and add Box
ledger_old = """        // Ledger
        val dateFormat = SimpleDateFormat("dd MMM, HH:mm", Locale.getDefault())
        LazyColumn(
            modifier = Modifier.weight(1f),
            reverseLayout = true
        ) {"""
ledger_new = """        // Ledger
        val dateFormat = SimpleDateFormat("dd MMM, HH:mm", Locale.getDefault())
        Box(modifier = Modifier.weight(1f)) {
            LazyColumn(
                state = listState,
                modifier = Modifier.fillMaxSize(),
                reverseLayout = true
            ) {"""
content = content.replace(ledger_old, ledger_new)

# 4. Close Box and insert AnimatedVisibility
lazy_end_old = """                    }
                }
            }
        }
        
        Spacer(modifier = Modifier.height(8.dp))

        // Numpad"""
lazy_end_new = """                    }
                }
            }
        }
        
        AnimatedVisibility(
            visible = showScrollToLatest,
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .padding(16.dp)
        ) {
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .background(MaterialTheme.colorScheme.surfaceVariant, RectangleShape)
                    .border(2.dp, MaterialTheme.colorScheme.outline, RectangleShape)
                    .clickable {
                        coroutineScope.launch {
                            listState.animateScrollToItem(0)
                        }
                    },
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Default.KeyboardArrowDown,
                    contentDescription = "Jump to Latest",
                    tint = MaterialTheme.colorScheme.onSurface
                )
            }
        }
    }
        
        Spacer(modifier = Modifier.height(8.dp))

        // Numpad"""
content = content.replace(lazy_end_old, lazy_end_new)

with open("app/src/main/java/com/example/ui/screens/BurnRateTrackerUI.kt", "w") as f:
    f.write(content)

