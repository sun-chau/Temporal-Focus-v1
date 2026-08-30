import re
with open('app/src/test/java/com/example/ui/screens/ChronometerScreenTest.kt', 'r') as f:
    content = f.read()

# Replace any function passing 4 arguments to take 6.
# We'll just replace `onSubmit = { title, target, created, category ->`
# with `onSubmit = { title, target, created, category, tag, reminder ->`

content = re.sub(
    r'onSubmit = \{ (.*?),(.*?),(.*?),(.*?) ->',
    r'onSubmit = { \1, \2, \3, \4, _, _ ->',
    content
)

# Or maybe it's just `_ , _, _, _ ->`
content = content.replace('_, _, _, _ ->', '_, _, _, _, _, _ ->')
content = content.replace('title, target, created, category ->', 'title, target, created, category, _, _ ->')

with open('app/src/test/java/com/example/ui/screens/ChronometerScreenTest.kt', 'w') as f:
    f.write(content)
