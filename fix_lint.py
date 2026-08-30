with open("app/build.gradle.kts", "r") as f:
    content = f.read()

if "fragment-ktx" not in content:
    content = content.replace("dependencies {", "dependencies {\n    implementation(\"androidx.fragment:fragment-ktx:1.8.0\")")
    with open("app/build.gradle.kts", "w") as f:
        f.write(content)
