sed -i 's/        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),//g' app/src/main/java/com/example/ui/screens/CheckInsScreen.kt
sed -i 's/        shape = RoundedCornerShape(16.dp)/        .clip(RoundedCornerShape(24.dp))\n            .background(Color(0xFF161616))\n            .border(1.dp, Color.White.copy(alpha=0.05f), RoundedCornerShape(24.dp))\n            .clickable(onClick = onClick)\n            .padding(24.dp)/g' app/src/main/java/com/example/ui/screens/CheckInsScreen.kt
sed -i 's/    Card(/    Box(/g' app/src/main/java/com/example/ui/screens/CheckInsScreen.kt
sed -i 's/            .clickable(onClick = onClick),//g' app/src/main/java/com/example/ui/screens/CheckInsScreen.kt
sed -i 's/        Column(modifier = Modifier.padding(16.dp)) {/        Column {/g' app/src/main/java/com/example/ui/screens/CheckInsScreen.kt
