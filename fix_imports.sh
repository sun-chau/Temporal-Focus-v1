sed -i '1d' app/src/main/java/com/example/ui/screens/CheckInsScreen.kt
sed -i '/package com.example.ui.screens/a import androidx.compose.foundation.border' app/src/main/java/com/example/ui/screens/CheckInsScreen.kt
sed -i '1d; 2d' app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt
sed -i '/package com.example.ui.screens/a import androidx.compose.foundation.border' app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt
sed -i '/package com.example.ui.screens/a import androidx.compose.ui.graphics.Color' app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt
