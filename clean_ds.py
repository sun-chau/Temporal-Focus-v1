import re

with open("/tmp/ds_recurrence_ui.txt", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    # Match the line number block and discard it, keeping the rest
    m = re.match(r"^\s*\d+\t(.*)", line)
    if m:
        new_lines.append(m.group(1) + "\n")
    else:
        # Check if it was space separated
        m2 = re.match(r"^\s*\d+\s+(.*)", line)
        if m2:
            new_lines.append(m2.group(1) + "\n")
        else:
            new_lines.append(line)

with open("/tmp/ds_recurrence_ui_clean.txt", "w") as f:
    f.writelines(new_lines)
