with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()
    
content = content.replace("    fun deleteAccount() {", "        }\n    }\n\n    fun deleteAccount() {")
content = content.replace("if (currentLabels.remove(category))", "if (currentLabels.remove(label))")

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
    f.write(content)
