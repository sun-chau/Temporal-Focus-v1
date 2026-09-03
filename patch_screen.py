import re

with open('app/src/main/java/com/example/ui/screens/CheckInsScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
"""            // Horizontal chip row
            import androidx.compose.foundation.horizontalScroll
            import androidx.compose.foundation.rememberScrollState
            Row(""",
"""            // Horizontal chip row
            Row("""
)

# And add the imports at the top
content = content.replace('import androidx.compose.foundation.layout.*', 'import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.horizontalScroll\nimport androidx.compose.foundation.rememberScrollState')

with open('app/src/main/java/com/example/ui/screens/CheckInsScreen.kt', 'w') as f:
    f.write(content)
