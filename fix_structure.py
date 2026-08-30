import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# 1. Extract pointerInput from Canvas Body
pointer_match = re.search(r'(\.pointerInput\(Unit\) \{\s*detectHorizontalDragGestures\(.*?onHorizontalDrag = \{.*?\}\s*\)\s*\})', content, re.DOTALL)
if not pointer_match:
    print("Could not find pointerInput")
    exit(1)

pointer_input_block = pointer_match.group(1)

# Remove it from the Canvas Body Box
content = content.replace(pointer_input_block, "")

# 2. Extract horizontalScroll from Canvas Body Box
content = content.replace('.horizontalScroll(horizontalScrollState)', '')

# 3. Extract horizontalScroll from TimelineRuler Box
content = content.replace('androidx.compose.foundation.layout.Box(modifier = Modifier.horizontalScroll(horizontalScrollState)) {\n                TimelineRuler(uiState.use24HourFormat)\n                }', 'TimelineRuler(uiState.use24HourFormat)')

# 4. Find the Box(weight=1f, fillMaxWidth) and add pointerInput
# It currently looks like:
#                         Box(
#                 modifier = Modifier
#                     .weight(1f)
#                     .fillMaxWidth()
#                                 ) {

target_box = """                        Box(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                                ) {"""
                                
replacement_box = f"""                        Box(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                    {pointer_input_block}
                                ) {{"""
                                
content = content.replace(target_box, replacement_box)

# 5. Add horizontalScroll back to the Column
target_col = """                            Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .offset { androidx.compose.ui.unit.IntOffset(overscrollOffset.toInt(), 0) }
                                        ) {"""

replacement_col = """                            Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .offset { androidx.compose.ui.unit.IntOffset(overscrollOffset.toInt(), 0) }
                        .horizontalScroll(horizontalScrollState)
                                        ) {"""

content = content.replace(target_col, replacement_col)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)

print("Fix applied")
