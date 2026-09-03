import re

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()

# Remove Tracker methods from MainViewModel
methods_to_remove = [
    r'fun getParsedPayload\(.*?}\s*}\s*}',
    r'fun updateGymPayload\(.*?\)\s*{.*?}',
    r'fun updateSyllabusPayload\(.*?\)\s*{.*?}',
    r'fun updateCustomPayload\(.*?\)\s*{.*?}',
    r'fun updateAssignmentPayload\(.*?\)\s*{.*?}',
    r'fun insertTracker\(.*?\)\s*{.*?}',
    r'fun updateTracker\(.*?\)\s*{.*?}',
    r'fun deleteTracker\(.*?\)\s*{.*?}'
]

for method_pattern in methods_to_remove:
    content = re.sub(method_pattern, '', content, flags=re.DOTALL)

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
    f.write(content)

