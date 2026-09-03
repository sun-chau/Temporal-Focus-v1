import re
with open("app/src/main/java/com/example/data/TrackerEntity.kt", "r") as f:
    content = f.read()

old_custom_payload = "data class CustomPayload(val schema: List<CustomField> = emptyList(), val entries: List<Map<String, String>> = emptyList())"
new_custom_payload = """data class CustomPayload(val schema: List<CustomField> = emptyList(), val entries: List<CustomEntry> = emptyList())
data class CustomEntry(val id: String = UUID.randomUUID().toString(), val timestampEpoch: Long, val fieldData: Map<String, String>)"""

content = content.replace(old_custom_payload, new_custom_payload)

with open("app/src/main/java/com/example/data/TrackerEntity.kt", "w") as f:
    f.write(content)
