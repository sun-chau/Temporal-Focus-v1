import re

with open('app/src/main/java/com/example/data/AppDatabase.kt', 'r') as f:
    content = f.read()

content = content.replace(', TrackerLogEntity::class', '')
content = content.replace('TrackerLogEntity::class, ', '')
content = content.replace('TrackerLogEntity::class', '')

if 'TypeConverters' not in content:
    content = content.replace('import androidx.room.RoomDatabase', 'import androidx.room.RoomDatabase\nimport androidx.room.TypeConverters')
    content = content.replace('@Database', '@TypeConverters(Converters::class)\n@Database')

with open('app/src/main/java/com/example/data/AppDatabase.kt', 'w') as f:
    f.write(content)
