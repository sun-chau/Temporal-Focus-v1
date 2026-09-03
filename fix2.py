import re
with open("app/src/main/java/com/example/viewmodel/TrackerViewModel.kt", "r") as f:
    content = f.read()

new_impl = """    fun getParsedPayload(entity: TrackerEntity): Any? {
        return try {
            val json = if (entity.payloadData.isBlank() || entity.payloadData == "{}") null else entity.payloadData
            when (entity.type) {
                TrackerType.GYM -> json?.let { gson.fromJson(it, GymPayload::class.java) } ?: GymPayload()
                TrackerType.SYLLABUS -> json?.let { gson.fromJson(it, SyllabusPayload::class.java) } ?: SyllabusPayload()
                TrackerType.CUSTOM -> json?.let { gson.fromJson(it, CustomPayload::class.java) } ?: CustomPayload()
                TrackerType.ASSIGNMENT -> json?.let { gson.fromJson(it, AssignmentPayload::class.java) } ?: AssignmentPayload()
            }
        } catch (e: Exception) {
            null
        }
    }"""
content = re.sub(r'fun getParsedPayload\(.*?\}\s*\}', new_impl, content, flags=re.DOTALL)
with open("app/src/main/java/com/example/viewmodel/TrackerViewModel.kt", "w") as f:
    f.write(content)
