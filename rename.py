import os
import glob
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    new_content = content.replace('Reminder', 'Deadline')
    new_content = new_content.replace('reminder', 'deadline')
    new_content = new_content.replace('REMINDER', 'DEADLINE')

    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        return True
    return False

kt_files = glob.glob('app/src/main/java/**/*.kt', recursive=True)
for file in kt_files:
    process_file(file)

