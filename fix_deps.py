path = 'app/build.gradle.kts'
with open(path, 'r') as f:
    content = f.read()

content = content.replace("implementation(libs.androidx.core.ktx)", "implementation(libs.androidx.core.ktx)\n  implementation(\"androidx.biometric:biometric:1.2.0-alpha05\")")

with open(path, 'w') as f:
    f.write(content)
