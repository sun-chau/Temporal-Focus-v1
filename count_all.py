with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    text = f.read()

print(f"Braces {{: {text.count('{')}, }}: {text.count('}')}")
print(f"Parens (: {text.count('(')}, ): {text.count(')')}")
print(f"Brackets [: {text.count('[')}, ]: {text.count(']')}")
