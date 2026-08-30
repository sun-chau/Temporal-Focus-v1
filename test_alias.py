import re

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

new_logic = """
                        val pm = context.packageManager
                        val packageName = context.packageName
                        
                        val allAliases = listOf(
                            "MainActivityOrange",
                            "MainActivityObsidian",
                            "MainActivityDaylight",
                            "MainActivityMidnight",
                            "MainActivityNordic",
                            "MainActivityForest",
                            "MainActivityCrimson",
                            "MainActivityAmber",
                            "MainActivityMonochrome"
                        )
                        
                        val targetAlias = "MainActivity" + iconId.replaceFirstChar { it.uppercase() }
                        
                        // We must disable MainActivity if target is not orange?
                        // Wait, if target is orange, do we enable MainActivity and disable all aliases?
                        // "The application's core MainActivity starts and persists with the default Orange icon as its primary <activity> declaration... Below the main activity in the Manifest, an <activity-alias> tag must be declared for every single new icon variant listed in Section 2... Default State: Crucially, all activity aliases must have android:enabled="false" set in their initial manifest declaration."
                        // This implies orange has an alias too ("MainActivityOrange")! 
                        // Wait, Section 2 table: Baseline/Default -> @mipmap/ic_launcher_orange
                        // And Section 4 says: "all activity aliases must have android:enabled='false' set in their initial manifest declaration"
                        // That means orange alias is ALSO false initially.
                        
                        // So if we select orange, we can EITHER enable MainActivity and disable all aliases, OR disable MainActivity and enable MainActivityOrange.
                        // Let's just disable whatever was active and enable the new one.
                        
                        // Disable MainActivity to remove the default icon from launcher
                        pm.setComponentEnabledSetting(
                            android.content.ComponentName(packageName, "$packageName.MainActivity"),
                            if (iconId == "orange") android.content.pm.PackageManager.COMPONENT_ENABLED_STATE_ENABLED else android.content.pm.PackageManager.COMPONENT_ENABLED_STATE_DISABLED,
                            android.content.pm.PackageManager.DONT_KILL_APP
                        )
                        
                        for (alias in allAliases) {
                            val componentName = android.content.ComponentName(packageName, "$packageName.$alias")
                            pm.setComponentEnabledSetting(
                                componentName,
                                if (alias == targetAlias && iconId != "orange") android.content.pm.PackageManager.COMPONENT_ENABLED_STATE_ENABLED else android.content.pm.PackageManager.COMPONENT_ENABLED_STATE_DISABLED,
                                android.content.pm.PackageManager.DONT_KILL_APP
                            )
                        }
"""

content = re.sub(r'val pm = context\.packageManager.*?DONT_KILL_APP\n                        \)', new_logic, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)

