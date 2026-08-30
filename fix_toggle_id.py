import re

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

search_str = r'''        if \(currentIds\.contains\(id\)\) \{
            currentIds\.remove\(id\)
        \} else \{
            currentIds\.add\(id\)
            while \(currentIds\.size > maxSlots\) \{
                currentIds\.removeAt\(0\) // FIFO
            \}
        \}'''

replace_str = '''        if (currentIds.contains(id)) {
            currentIds.remove(id)
        } else {
            currentIds.add(id)
            if (maxSlots != -1) {
                while (currentIds.size > maxSlots) {
                    currentIds.removeAt(0) // FIFO
                }
            }
        }'''

content = re.sub(search_str, replace_str, content)

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
