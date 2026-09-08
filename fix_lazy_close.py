import re

with open("app/src/main/java/com/example/ui/screens/BurnRateTrackerUI.kt", "r") as f:
    content = f.read()

old_block = """                    }
                }
            }
        
            AnimatedVisibility("""

new_block = """                    }
                }
            }
            } // end LazyColumn
        
            AnimatedVisibility("""

content = content.replace(old_block, new_block)

# Since I added an extra `}`, I need to remove one from the end of the Box.
old_block2 = """            }
        }
        }
        
        Spacer(modifier = Modifier.height(8.dp))"""

new_block2 = """            }
        }
        
        Spacer(modifier = Modifier.height(8.dp))"""

content = content.replace(old_block2, new_block2)

with open("app/src/main/java/com/example/ui/screens/BurnRateTrackerUI.kt", "w") as f:
    f.write(content)
