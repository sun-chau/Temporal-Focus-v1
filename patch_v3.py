import re

with open('app/src/main/java/com/example/ui/screens/LandscapeChronographScreen.kt', 'r') as f:
    content = f.read()

# Add missing imports
if "import androidx.compose.ui.draw.clip" not in content:
    content = content.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\nimport androidx.compose.ui.draw.clip\nimport androidx.compose.foundation.border\nimport androidx.compose.foundation.clickable\nimport androidx.compose.foundation.shape.CircleShape")

# Replace broken fully qualified names
broken = """            Box(
                modifier = Modifier
                    .androidx.compose.ui.draw.clip(androidx.compose.foundation.shape.CircleShape)
                    .androidx.compose.foundation.border(
                        1.dp, 
                        textColor.copy(alpha = 0.5f), 
                        androidx.compose.foundation.shape.CircleShape
                    )
                    .androidx.compose.foundation.clickable { is24HourFormat = !is24HourFormat }
                    .padding(horizontal = 16.dp, vertical = 8.dp),
                contentAlignment = Alignment.Center
            ) {"""

fixed = """            Box(
                modifier = Modifier
                    .clip(CircleShape)
                    .border(
                        1.dp, 
                        textColor.copy(alpha = 0.5f), 
                        CircleShape
                    )
                    .clickable { is24HourFormat = !is24HourFormat }
                    .padding(horizontal = 16.dp, vertical = 8.dp),
                contentAlignment = Alignment.Center
            ) {"""

content = content.replace(broken, fixed)

with open('app/src/main/java/com/example/ui/screens/LandscapeChronographScreen.kt', 'w') as f:
    f.write(content)
