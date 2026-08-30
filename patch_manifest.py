import re

with open("app/src/main/AndroidManifest.xml", "r") as f:
    content = f.read()

aliases = """
        <activity-alias
            android:name=".MainActivityOrange"
            android:enabled="false"
            android:exported="true"
            android:icon="@mipmap/ic_launcher_orange"
            android:roundIcon="@mipmap/ic_launcher_orange_round"
            android:targetActivity=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity-alias>
        <activity-alias
            android:name=".MainActivityObsidian"
            android:enabled="false"
            android:exported="true"
            android:icon="@mipmap/ic_launcher_obsidian"
            android:roundIcon="@mipmap/ic_launcher_obsidian_round"
            android:targetActivity=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity-alias>
        <activity-alias
            android:name=".MainActivityDaylight"
            android:enabled="false"
            android:exported="true"
            android:icon="@mipmap/ic_launcher_daylight"
            android:roundIcon="@mipmap/ic_launcher_daylight_round"
            android:targetActivity=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity-alias>
        <activity-alias
            android:name=".MainActivityMidnight"
            android:enabled="false"
            android:exported="true"
            android:icon="@mipmap/ic_launcher_midnight"
            android:roundIcon="@mipmap/ic_launcher_midnight_round"
            android:targetActivity=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity-alias>
        <activity-alias
            android:name=".MainActivityNordic"
            android:enabled="false"
            android:exported="true"
            android:icon="@mipmap/ic_launcher_nordic"
            android:roundIcon="@mipmap/ic_launcher_nordic_round"
            android:targetActivity=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity-alias>
        <activity-alias
            android:name=".MainActivityForest"
            android:enabled="false"
            android:exported="true"
            android:icon="@mipmap/ic_launcher_forest"
            android:roundIcon="@mipmap/ic_launcher_forest_round"
            android:targetActivity=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity-alias>
        <activity-alias
            android:name=".MainActivityCrimson"
            android:enabled="false"
            android:exported="true"
            android:icon="@mipmap/ic_launcher_crimson"
            android:roundIcon="@mipmap/ic_launcher_crimson_round"
            android:targetActivity=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity-alias>
        <activity-alias
            android:name=".MainActivityAmber"
            android:enabled="false"
            android:exported="true"
            android:icon="@mipmap/ic_launcher_amber"
            android:roundIcon="@mipmap/ic_launcher_amber_round"
            android:targetActivity=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity-alias>
        <activity-alias
            android:name=".MainActivityMonochrome"
            android:enabled="false"
            android:exported="true"
            android:icon="@mipmap/ic_launcher_monochrome"
            android:roundIcon="@mipmap/ic_launcher_monochrome_round"
            android:targetActivity=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity-alias>
"""

content = content.replace("</activity>", "</activity>" + aliases)

with open("app/src/main/AndroidManifest.xml", "w") as f:
    f.write(content)

