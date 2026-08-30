import re

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    content = f.read()

# Remove the FloatingActionButton
fab_pattern = r'\s*androidx\.compose\.material3\.FloatingActionButton\(.*?\)\s*\{\s*androidx\.compose\.material3\.Icon\(\s*androidx\.compose\.material\.icons\.Icons\.Default\.Add,\s*contentDescription = "Quick Deadline"\s*\)\s*\}'

content = re.sub(fab_pattern, '', content, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(content)
