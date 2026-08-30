import re

with open('app/src/main/java/com/example/data/AppSettings.kt', 'r') as f:
    content = f.read()

new_fields = """    var securityQuestion: String
        get() = prefs.getString("security_question", "") ?: ""
        set(value) = prefs.edit().putString("security_question", value).apply()
        
    var securityAnswer: String
        get() = prefs.getString("security_answer", "") ?: ""
        set(value) = prefs.edit().putString("security_answer", value).apply()
        
    var securityQuestion2: String
        get() = prefs.getString("security_question2", "") ?: ""
        set(value) = prefs.edit().putString("security_question2", value).apply()
        
    var securityAnswer2: String
        get() = prefs.getString("security_answer2", "") ?: ""
        set(value) = prefs.edit().putString("security_answer2", value).apply()
        
    var securityQuestion3: String
        get() = prefs.getString("security_question3", "") ?: ""
        set(value) = prefs.edit().putString("security_question3", value).apply()
        
    var securityAnswer3: String
        get() = prefs.getString("security_answer3", "") ?: ""
        set(value) = prefs.edit().putString("security_answer3", value).apply()"""

old_fields = """    var securityQuestion: String
        get() = prefs.getString("security_question", "") ?: ""
        set(value) = prefs.edit().putString("security_question", value).apply()
        
    var securityAnswer: String
        get() = prefs.getString("security_answer", "") ?: ""
        set(value) = prefs.edit().putString("security_answer", value).apply()"""

content = content.replace(old_fields, new_fields)
with open('app/src/main/java/com/example/data/AppSettings.kt', 'w') as f:
    f.write(content)
