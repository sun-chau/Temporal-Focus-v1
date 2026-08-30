import sys
import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# 1. Update TimelineRuler
# Remove Text("half"...) block
pattern_half_text = r'''\s*Text\(\s*text = "half",\s*fontSize = 8\.sp,\s*color = MaterialTheme\.colorScheme\.onSurface\.copy\(alpha = 0\.5f\),\s*modifier = Modifier\.offset\(x = minorOffset \+ 2\.dp, y = 14\.dp\)\s*\)'''
content = re.sub(pattern_half_text, "", content)

# Update major tick in TimelineRuler:
# We find the Box right after "// Major tick"
pattern_ruler_major = r'''(// Major tick\s*Box\(\s*modifier = Modifier\s*\.offset\(x = offset\)\s*\.width\()1\.dp(\)\s*\.fillMaxHeight\(\)\s*\.background\(MaterialTheme\.colorScheme\.onSurface\.copy\(alpha = 0\.3f\)\)\s*\))'''
content = re.sub(pattern_ruler_major, r'\g<1>2.dp\g<2>', content)

# Update major tick in TimelineGrid:
# We find the Box right after "// Major tick line"
pattern_grid_major = r'''(// Major tick line\s*Box\(\s*modifier = Modifier\s*\.offset\(x = offset\)\s*\.width\()1\.dp(\)\s*\.fillMaxHeight\(\)\s*\.background\(MaterialTheme\.colorScheme\.onSurface\.copy\(alpha = 0\.08f\)\)\s*\))'''
content = re.sub(pattern_grid_major, r'\g<1>2.dp\g<2>', content)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
