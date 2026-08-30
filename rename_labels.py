import os
import re

replacements = [
    ("customTags", "customLabels"),
    ("customCategories", "customLabels"),
    ("coloredTagsEnabled", "coloredLabelsEnabled"),
    ("coloredCategoriesEnabled", "coloredLabelsEnabled"),
    ("addCustomTag", "addCustomLabel"),
    ("removeCustomTag", "removeCustomLabel"),
    ("addCustomCategory", "addCustomLabel"),
    ("removeCustomCategory", "removeCustomLabel"),
    
    ("val tags: String", "val labels: String"),
    ("val tag: String", "val label: String"),
    ("tag = tag", "label = label"),
    ("tags = tags", "labels = labels"),
    ("tag = draft.tag", "label = draft.label"),
    ("tags = draft.tags", "labels = draft.labels"),
    ("tag = :tag", "label = :label"),
    ("tag: String", "label: String"),
    ("tags: String", "labels: String"),
    ("tag = \"\"", "label = \"\""),
    ("tags = \"\"", "labels = \"\""),
    ("tag = \"None\"", "labels = \"None\""),
    ("tag = tag,", "label = label,"),
    ("tags = tags,", "labels = labels,"),
    ("task.tag", "task.label"),
    ("task.tags", "task.labels"),
    ("draft.tag", "draft.label"),
    ("draft.tags", "draft.labels"),
    ("TagUtils", "LabelUtils"),
    ("getTagColor", "getLabelColor"),
    ("getTagName", "getLabelName"),
    
    ("\"Tags\"", "\"Labels\""),
    ("\"Tag\"", "\"Label\""),
    ("\"Categories\"", "\"Labels\""),
    ("\"Category\"", "\"Label\""),
    ("\"Tags & Categories\"", "\"Labels\""),
    ("\"Categories & Tags\"", "\"Labels\""),
    
    ("custom_tags", "custom_labels"),
    ("custom_categories", "custom_labels"),
    ("colored_tags_enabled", "colored_labels_enabled"),
    ("colored_categories_enabled", "colored_labels_enabled"),
]

for root, dirs, files in os.walk('app/src/main/java/'):
    for file in files:
        if file.endswith('.kt'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            
            new_content = content
            for old, new in replacements:
                new_content = new_content.replace(old, new)
                
            if content != new_content:
                with open(filepath, 'w') as f:
                    f.write(new_content)
