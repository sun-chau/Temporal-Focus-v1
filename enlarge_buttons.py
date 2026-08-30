import sys
import re

files = [
    "app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt",
    "app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt"
]

for file_path in files:
    with open(file_path, "r") as f:
        content = f.read()

    # We need to replace specifically the + and - buttons under "Number of occurrences"
    # To be safe, we will just find the `size(48.dp)` and `fontSize = 28.sp` near the occurrences logic.
    # Actually, are there other minus and plus buttons with size 48 in these files? Let's check.
    
    # We can use regex to replace the specific boxes
    box_pattern = r'''(Box\(\s*modifier = Modifier\s*\.size\()48\.dp(\)\s*\.clip\(CircleShape\)\s*\.background\(MaterialTheme\.colorScheme\.surfaceVariant\)\s*\.pointerInput\(Unit\) \{\s*detectTapGestures\(\s*onPress = \{\s*(minusHolding|plusHolding) = true\s*tryAwaitRelease\(\)\s*\3 = false\s*\}\s*\)\s*\},\s*contentAlignment = Alignment\.Center\s*\)\s*\{\s*Text\("(-|\+)", fontSize = )28\.sp(,\s*color = MaterialTheme\.colorScheme\.primary, fontWeight = FontWeight\.Bold\)\s*\})'''
    
    content = re.sub(box_pattern, r'\g<1>64.dp\g<2>36.sp\g<4>', content)
    
    # And the text between them: text = if (occurrenceCount <= 0) "∞" else "$occurrenceCount", fontWeight = FontWeight.Bold, fontSize = 20.sp,
    text_pattern = r'''(text = if \(occurrenceCount <= 0\) "∞" else "\$occurrenceCount",\s*fontWeight = FontWeight\.Bold,\s*fontSize = )20\.sp(,)'''
    content = re.sub(text_pattern, r'\g<1>24.sp\g<2>', content)

    with open(file_path, "w") as f:
        f.write(content)

