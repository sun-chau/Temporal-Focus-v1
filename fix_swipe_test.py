import re

with open("app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt", "r") as f:
    content = f.read()

search_str = r'''        backgroundContent = \{
            val direction = dismissState\.dismissDirection
            val color by androidx\.compose\.animation\.animateColorAsState\('''

replace_str = '''        backgroundContent = {
            val direction = dismissState.dismissDirection
            val isSwipingRight = dismissState.targetValue == SwipeToDismissBoxValue.StartToEnd || (dismissState.progress < 1f && dismissState.dismissDirection == SwipeToDismissBoxValue.StartToEnd)
            // fallback
            
            val color by androidx.compose.animation.animateColorAsState('''

content = re.sub(search_str, replace_str, content)
