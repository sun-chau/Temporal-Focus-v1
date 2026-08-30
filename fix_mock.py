import re

with open('app/src/main/java/com/example/data/MockDataGenerator.kt', 'r') as f:
    content = f.read()

content = content.replace('tag = "', 'label = "')
content = content.replace('tags = "', 'labels = "')

with open('app/src/main/java/com/example/data/MockDataGenerator.kt', 'w') as f:
    f.write(content)
