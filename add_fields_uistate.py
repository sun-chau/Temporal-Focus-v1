import re

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()

# Replace UiState
old_uistate = """    val securityQuestion: String = "",
    val securityAnswer: String = "",
    val biometricsEnabled: Boolean = false,"""

new_uistate = """    val securityQuestion: String = "",
    val securityAnswer: String = "",
    val securityQuestion2: String = "",
    val securityAnswer2: String = "",
    val securityQuestion3: String = "",
    val securityAnswer3: String = "",
    val biometricsEnabled: Boolean = false,"""
content = content.replace(old_uistate, new_uistate)

# Replace appSettings to UiState initialization
old_init = """            securityQuestion = appSettings.securityQuestion,
            securityAnswer = appSettings.securityAnswer,
            biometricsEnabled = appSettings.biometricsEnabled,"""

new_init = """            securityQuestion = appSettings.securityQuestion,
            securityAnswer = appSettings.securityAnswer,
            securityQuestion2 = appSettings.securityQuestion2,
            securityAnswer2 = appSettings.securityAnswer2,
            securityQuestion3 = appSettings.securityQuestion3,
            securityAnswer3 = appSettings.securityAnswer3,
            biometricsEnabled = appSettings.biometricsEnabled,"""
content = content.replace(old_init, new_init)

# Check setSecurityQuestionAndAnswer and replace
old_set_q = """    fun setSecurityQuestionAndAnswer(question: String, answer: String) {
        appSettings.securityQuestion = question
        appSettings.securityAnswer = answer
        _uiState.update { it.copy(securityQuestion = question, securityAnswer = answer) }
    }"""
new_set_q = """    fun setSecurityQuestionsAndAnswers(q1: String, a1: String, q2: String, a2: String, q3: String, a3: String) {
        appSettings.securityQuestion = q1
        appSettings.securityAnswer = a1
        appSettings.securityQuestion2 = q2
        appSettings.securityAnswer2 = a2
        appSettings.securityQuestion3 = q3
        appSettings.securityAnswer3 = a3
        _uiState.update { it.copy(
            securityQuestion = q1, securityAnswer = a1,
            securityQuestion2 = q2, securityAnswer2 = a2,
            securityQuestion3 = q3, securityAnswer3 = a3
        ) }
    }"""
if old_set_q in content:
    content = content.replace(old_set_q, new_set_q)
else:
    print("setSecurityQuestionAndAnswer not found, looking for regex")
    
with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
    f.write(content)
