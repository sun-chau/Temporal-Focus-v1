import re

def remove_fab(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    # Find the FloatingActionButton block
    fab_pattern = r'(\s*)FloatingActionButton\([\s\S]*?\)\s*\{[\s\S]*?\}'
    content = re.sub(fab_pattern, r'', content)

    with open(filepath, "w") as f:
        f.write(content)

remove_fab("app/src/main/java/com/example/ui/screens/BinaryTrackerUI.kt")
remove_fab("app/src/main/java/com/example/ui/screens/VolumeTrackerUI.kt")
