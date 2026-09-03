import re

with open("app/src/main/java/com/example/viewmodel/TrackerViewModel.kt", "r") as f:
    content = f.read()

del_tag_func = """
    fun deleteBurnRateTag(tracker: TrackerEntity, tagToDelete: String) {
        val payload = getParsedPayload(tracker) as? BurnRatePayload ?: return
        val updatedTags = payload.customTags - tagToDelete
        updateBurnRatePayload(tracker, payload.copy(customTags = updatedTags))
    }
"""

if "fun deleteBurnRateTag" not in content:
    content = content.replace("    fun updateBurnRatePayload", del_tag_func + "    fun updateBurnRatePayload")

with open("app/src/main/java/com/example/viewmodel/TrackerViewModel.kt", "w") as f:
    f.write(content)
