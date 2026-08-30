with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if "fun deleteAccount" in line:
        skip = False
    
    if skip and line.strip() == "}":
        continue
        
    new_lines.append(line)
    
    if "fun removeCustomLabel" in line:
        skip = True

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
    f.writelines(new_lines)
