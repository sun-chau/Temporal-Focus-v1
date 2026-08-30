with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    lines = f.readlines()

density_lines = []
new_lines = []
skip = False
for line in lines:
    if "val density = LocalDensity.current" in line:
        density_lines.append(line)
        skip = True
    elif skip and "val configuration = LocalConfiguration.current" in line:
        density_lines.append(line)
    elif skip and "val screenWidthPx = with(density) { configuration.screenWidthDp.dp.toPx() }" in line:
        density_lines.append(line)
    elif skip and "val screenWidthDp = configuration.screenWidthDp" in line:
        density_lines.append(line)
        skip = False
    else:
        new_lines.append(line)

# find the place to insert it: right after `val context = LocalContext.current`
insert_idx = 0
for i, line in enumerate(new_lines):
    if "val context = LocalContext.current" in line:
        insert_idx = i + 1
        break

new_lines = new_lines[:insert_idx] + density_lines + new_lines[insert_idx:]

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.writelines(new_lines)
