import re
with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

# Replace first launch
content = content.replace("viewModelScope.launch {\n            val count = journalDao.getTemplateCount()", "viewModelScope.launch(Dispatchers.IO) {\n            val count = journalDao.getTemplateCount()")

# Replace second/third launch
target = """        viewModelScope.launch {
            
        viewModelScope.launch {
            while (true) {"""
replacement = """        viewModelScope.launch(Dispatchers.IO) {
            
        viewModelScope.launch(Dispatchers.IO) {
            while (true) {"""
content = content.replace(target, replacement)

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
