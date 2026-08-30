import os

themes = [
    ("orange", "#FFFF8C00"),
    ("obsidian", "#888888"),
    ("daylight", "#4FC3F7"),
    ("midnight", "#FFFFFF"),
    ("nordic", "#00BFA5"),
    ("forest", "#2E7D32"),
    ("crimson", "#D50000"),
    ("amber", "#FFB300"),
    ("monochrome", "#9E9E9E")
]

background_color = "#18181B"

os.makedirs("app/src/main/res/drawable", exist_ok=True)
os.makedirs("app/src/main/res/mipmap-anydpi-v26", exist_ok=True)
os.makedirs("app/src/main/res/mipmap", exist_ok=True)

for name, color in themes:
    fg_content = f"""<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="{color}"
        android:pathData="M34,24 h40 v10 l-15,20 l15,20 v10 h-40 v-10 l15,-20 l-15,-20 z" />
</vector>"""
    with open(f"app/src/main/res/drawable/ic_launcher_foreground_{name}.xml", "w") as f:
        f.write(fg_content)

    adaptive_content = f"""<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background" />
    <foreground android:drawable="@drawable/ic_launcher_foreground_{name}" />
    <monochrome android:drawable="@drawable/ic_launcher_foreground_{name}" />
</adaptive-icon>"""
    with open(f"app/src/main/res/mipmap-anydpi-v26/ic_launcher_{name}.xml", "w") as f:
        f.write(adaptive_content)
    with open(f"app/src/main/res/mipmap-anydpi-v26/ic_launcher_{name}_round.xml", "w") as f:
        f.write(adaptive_content)

    legacy_content = f"""<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="48dp"
    android:height="48dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path android:fillColor="{background_color}" android:pathData="M0,0h108v108h-108z"/>
    <path android:fillColor="{color}" android:pathData="M34,24 h40 v10 l-15,20 l15,20 v10 h-40 v-10 l15,-20 l-15,-20 z" />
</vector>"""
    with open(f"app/src/main/res/mipmap/ic_launcher_{name}.xml", "w") as f:
        f.write(legacy_content)
    with open(f"app/src/main/res/mipmap/ic_launcher_{name}_round.xml", "w") as f:
        f.write(legacy_content)

