with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

content = content.replace("""                    iterations++
                }
            }
        }
        recalculateAllLanes(db)
        clearDailyScheduleDraft()""", """                    iterations++
                }
            }
            recalculateAllLanes(db)
        }
        clearDailyScheduleDraft()""")

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
