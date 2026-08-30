with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

import re
old_str = """                        if (isToday) {
                            NowLine()
                        }
                    }
                }
                }
                }
            }
        }
    }
        if (reschedulingSchedule != null) {"""

new_str = """                        if (isToday) {
                            NowLine()
                        }
                    }
                }
                }
                }
            }
        }
        if (reschedulingSchedule != null) {"""

content = content.replace(old_str, new_str)
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
