import re

with open("app/src/main/java/com/example/ui/screens/BurnRateTrackerUI.kt", "r") as f:
    content = f.read()

old_block = """        // Top Fraction
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .border(2.dp, MaterialTheme.colorScheme.outline, RectangleShape)
                .clickable { showLimitDialog = true }
                .padding(16.dp),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = "₹%.2f / ₹%.2f".format(monthlySum, payload.monthlyLimit),
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold,
                fontFamily = FontFamily.Monospace,
                color = if (payload.monthlyLimit > 0.0 && monthlySum > payload.monthlyLimit) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.onSurface,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        }"""

new_block = """        // Top Fraction
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .border(2.dp, MaterialTheme.colorScheme.outline, RectangleShape)
                .clickable { showLimitDialog = true }
                .padding(16.dp),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = "₹%.2f / ₹%.2f".format(monthlySum, payload.monthlyLimit),
                modifier = Modifier.horizontalScroll(rememberScrollState()),
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold,
                fontFamily = FontFamily.Monospace,
                color = if (payload.monthlyLimit > 0.0 && monthlySum > payload.monthlyLimit) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.onSurface,
                maxLines = 1
            )
        }"""

content = content.replace(old_block, new_block)

with open("app/src/main/java/com/example/ui/screens/BurnRateTrackerUI.kt", "w") as f:
    f.write(content)

