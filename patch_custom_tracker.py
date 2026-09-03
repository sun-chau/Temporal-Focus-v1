import re

with open('app/src/main/java/com/example/data/TrackerEntities.kt', 'a') as f:
    f.write("\n")
    f.write("data class CustomPayload(val schema: List<CustomField> = emptyList(), val entries: List<Map<String, String>> = emptyList())\n")
    f.write("data class CustomField(val id: String = UUID.randomUUID().toString(), val label: String, val fieldType: CustomFieldType)\n")
    f.write("enum class CustomFieldType { NUMBER, TEXT, CHECKBOX }\n")
