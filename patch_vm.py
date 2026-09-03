import re

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()

content = re.sub(r'val trackerLogs: StateFlow<List<com\.example\.data\.TrackerLogEntity>>\s*', '', content)
content = re.sub(r'trackerLogs = trackerDao\.getAllLogs\(\)\.stateIn\(viewModelScope, SharingStarted\.WhileSubscribed\(5000\), emptyList\(\)\)\s*', '', content)

# Remove the old functions
content = re.sub(r'fun logTrackerVolume.*?(?=fun spendBankedDay|fun acceptBreak|$)', '', content, flags=re.DOTALL)
content = re.sub(r'fun spendBankedDay.*?(?=fun acceptBreak|$)', '', content, flags=re.DOTALL)
content = re.sub(r'fun acceptBreak.*?}\s*}', '', content, flags=re.DOTALL)

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
    f.write(content)
