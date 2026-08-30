find app/src/main/java/com/example/ui/screens/ -type f -name "*.kt" -exec sed -i \
  -e 's/Color(0xFF1E1E1E)/MaterialTheme.colorScheme.surfaceVariant/g' \
  -e 's/Color(0xFF161616)/MaterialTheme.colorScheme.surfaceVariant/g' \
  -e 's/Color(0xFF222222)/MaterialTheme.colorScheme.surfaceVariant/g' \
  -e 's/Color(0xFF252525)/MaterialTheme.colorScheme.surfaceVariant/g' \
  -e 's/Color(0xFF2A2A2A)/MaterialTheme.colorScheme.surfaceVariant/g' \
  -e 's/Color(0xFF1A1A1A)/MaterialTheme.colorScheme.surfaceVariant/g' \
  -e 's/Color(0xFF111111)/MaterialTheme.colorScheme.surfaceVariant/g' \
  -e 's/Color(0xFF333333)/MaterialTheme.colorScheme.surfaceVariant/g' \
  -e 's/Color(0xFF121212)/MaterialTheme.colorScheme.surface/g' \
  -e 's/Color.White/MaterialTheme.colorScheme.onSurface/g' \
  -e 's/Color.Gray/MaterialTheme.colorScheme.onSurfaceVariant/g' \
  -e 's/Color.LightGray/MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f)/g' \
  -e 's/Color.DarkGray/MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.3f)/g' \
  -e 's/Color.Black/MaterialTheme.colorScheme.onSurface/g' \
  {} +
