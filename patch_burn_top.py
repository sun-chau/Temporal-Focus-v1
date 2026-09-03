import re

with open("app/src/main/java/com/example/ui/screens/BurnRateTrackerUI.kt", "r") as f:
    content = f.read()

old_block = """        // Top Fraction
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(
                text = "₹%.2f / ₹%.2f".format(monthlySum, payload.monthlyLimit),
                style = MaterialTheme.typography.displaySmall,
                fontWeight = FontWeight.Bold,
                fontFamily = FontFamily.Monospace,
                color = if (payload.monthlyLimit > 0.0 && monthlySum > payload.monthlyLimit) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.onSurface
            )
            IconButton(onClick = { showLimitDialog = true }) {
                Icon(Icons.Filled.Edit, contentDescription = "Edit Limit")
            }
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
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold,
                fontFamily = FontFamily.Monospace,
                color = if (payload.monthlyLimit > 0.0 && monthlySum > payload.monthlyLimit) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.onSurface,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        }"""

content = content.replace(old_block, new_block)

if "import androidx.compose.ui.graphics.RectangleShape" not in content:
    content = content.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\nimport androidx.compose.ui.graphics.RectangleShape\nimport androidx.compose.foundation.border")

with open("app/src/main/java/com/example/ui/screens/BurnRateTrackerUI.kt", "w") as f:
    f.write(content)

