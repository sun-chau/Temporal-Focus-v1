import re
with open("app/src/main/java/com/example/data/TrackerEntity.kt", "r") as f:
    content = f.read()

# Add ExerciseSet
if "data class ExerciseSet" not in content:
    content = content.replace(
        "data class GymPayload",
        "data class ExerciseSet(\n    val id: String = UUID.randomUUID().toString(),\n    val reps: Int,\n    val weightKg: Float? = null\n)\n\ndata class GymPayload"
    )

# Modify ExerciseLog
content = re.sub(
    r'val reps:\s*Int\?\s*=\s*null,',
    'val sets: List<ExerciseSet> = emptyList(),',
    content
)

with open("app/src/main/java/com/example/data/TrackerEntity.kt", "w") as f:
    f.write(content)
