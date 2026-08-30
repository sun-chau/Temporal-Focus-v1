import re

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'r') as f:
    content = f.read()

old_content = """@Composable
fun TacticalInfoSheetContent() {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 24.dp)
            .padding(bottom = 32.dp, top = 8.dp)
            .navigationBarsPadding()
            .verticalScroll(rememberScrollState())
    ) {
        Text(
            "TACTICAL HUD METRICS",
            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f),
            fontSize = 12.sp,
            fontWeight = FontWeight.Bold
        )
        Spacer(Modifier.height(16.dp))
        
        InfoAccordionItem("YIELD", "Tracks your current session progress against your total goal.", "S_{current} / S_{target}")
        InfoAccordionItem("INVESTED", "The total accumulated time you have spent strictly in the focus phase.", "Σ t_{focus}")
        InfoAccordionItem("INTERVENTIONS", "A discipline tracker measuring how many times you manually altered the timer during a live session.", "Σ N_{adjustments}")
        InfoAccordionItem("EFFICIENCY", "Your focus-to-rest ratio expressed as a percentage.", "(t_{focus} / t_{active}) × 100")
        InfoAccordionItem("DEVIATION", "The overall schedule drift. It mathematically compares your actual elapsed time against a perfect, uninterrupted schedule.", "Δt = t_{actual} - t_{ideal}")
        InfoAccordionItem("ETA", "The estimated real-world time your entire multi-session block will be completed.", "T_{eta} = T_{now} + t_{rem} + Σ t_{pending}")
    }
}

@Composable
fun InfoAccordionItem(title: String, description: String, formula: String) {
    var expanded by remember { mutableStateOf(false) }
    Column(modifier = Modifier.fillMaxWidth().clickable { expanded = !expanded }.padding(vertical = 12.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
            Text(title, fontFamily = FontFamily.Monospace, fontWeight = FontWeight.Bold, fontSize = 16.sp)
            Icon(
                imageVector = if (expanded) Icons.Default.ExpandLess else Icons.Default.ExpandMore, 
                contentDescription = null, 
                tint = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)
            )
        }
        if (expanded) {
            Column(modifier = Modifier.padding(top = 8.dp)) {
                Text(description, fontSize = 14.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Spacer(Modifier.height(12.dp))
                
                val annotatedMath = androidx.compose.ui.text.buildAnnotatedString {
                    var i = 0
                    while (i < formula.length) {
                        if (formula[i] == '_') {
                            i++
                            if (i < formula.length && formula[i] == '{') {
                                i++
                                val start = i
                                while (i < formula.length && formula[i] != '}') i++
                                val sub = formula.substring(start, i)
                                withStyle(androidx.compose.ui.text.SpanStyle(
                                    baselineShift = androidx.compose.ui.text.style.BaselineShift.Subscript, 
                                    fontSize = 12.sp,
                                    fontStyle = androidx.compose.ui.text.font.FontStyle.Normal
                                )) {
                                    append(sub)
                                }
                                if (i < formula.length) i++ // skip }
                            }
                        } else {
                            val c = formula[i]
                            if (c.isLetter() && c != 'Δ' && c != 'Σ') {
                                withStyle(androidx.compose.ui.text.SpanStyle(fontStyle = androidx.compose.ui.text.font.FontStyle.Italic)) {
                                    append(c.toString())
                                }
                            } else {
                                append(c.toString())
                            }
                            i++
                        }
                    }
                }
                
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(8.dp))
                        .background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.4f))
                        .padding(16.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = annotatedMath,
                        fontFamily = FontFamily.Serif,
                        fontSize = 18.sp,
                        color = MaterialTheme.colorScheme.onSurface,
                        letterSpacing = 1.sp
                    )
                }
                Spacer(Modifier.height(4.dp))
            }
        }
    }
    HorizontalDivider(color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f))
}"""

new_content = """@Composable
fun TacticalInfoSheetContent() {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 24.dp)
            .padding(bottom = 32.dp, top = 8.dp)
            .navigationBarsPadding()
            .verticalScroll(rememberScrollState())
    ) {
        Text(
            "TACTICAL HUD METRICS",
            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f),
            fontSize = 12.sp,
            fontWeight = FontWeight.Bold
        )
        Spacer(Modifier.height(16.dp))
        
        InfoAccordionItem("YIELD", "Tracks your current session progress against your total goal.") {
            MathFraction(
                numerator = { MathText("S_{current}") },
                denominator = { MathText("S_{target}") }
            )
        }
        InfoAccordionItem("INVESTED", "The total accumulated time you have spent strictly in the focus phase.") {
            MathText("Σ t_{focus}")
        }
        InfoAccordionItem("INTERVENTIONS", "A discipline tracker measuring how many times you manually altered the timer during a live session.") {
            MathText("Σ N_{adjustments}")
        }
        InfoAccordionItem("EFFICIENCY", "Your focus-to-rest ratio expressed as a percentage.") {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("(", fontFamily = FontFamily.Serif, fontSize = 24.sp, color = MaterialTheme.colorScheme.onSurface)
                MathFraction(
                    numerator = { MathText("t_{focus}") },
                    denominator = { MathText("t_{active}") }
                )
                Text(") × 100", fontFamily = FontFamily.Serif, fontSize = 18.sp, color = MaterialTheme.colorScheme.onSurface)
            }
        }
        InfoAccordionItem("DEVIATION", "The overall schedule drift. It mathematically compares your actual elapsed time against a perfect, uninterrupted schedule.") {
            MathText("Δt = t_{actual} - t_{ideal}")
        }
        InfoAccordionItem("ETA", "The estimated real-world time your entire multi-session block will be completed.") {
            MathText("T_{eta} = T_{now} + t_{rem} + Σ t_{pending}")
        }
    }
}

@Composable
fun MathFraction(numerator: @Composable () -> Unit, denominator: @Composable () -> Unit) {
    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.padding(horizontal = 6.dp)) {
        numerator()
        HorizontalDivider(modifier = Modifier.padding(vertical = 4.dp).width(40.dp), color = MaterialTheme.colorScheme.onSurface, thickness = 1.dp)
        denominator()
    }
}

@Composable
fun MathText(formula: String) {
    val annotatedMath = androidx.compose.ui.text.buildAnnotatedString {
        var i = 0
        while (i < formula.length) {
            if (formula[i] == '_') {
                i++
                if (i < formula.length && formula[i] == '{') {
                    i++
                    val start = i
                    while (i < formula.length && formula[i] != '}') i++
                    val sub = formula.substring(start, i)
                    withStyle(androidx.compose.ui.text.SpanStyle(
                        baselineShift = androidx.compose.ui.text.style.BaselineShift.Subscript, 
                        fontSize = 12.sp,
                        fontStyle = androidx.compose.ui.text.font.FontStyle.Normal
                    )) {
                        append(sub)
                    }
                    if (i < formula.length) i++ // skip }
                }
            } else {
                val c = formula[i]
                if (c.isLetter() && c != 'Δ' && c != 'Σ') {
                    withStyle(androidx.compose.ui.text.SpanStyle(fontStyle = androidx.compose.ui.text.font.FontStyle.Italic)) {
                        append(c.toString())
                    }
                } else {
                    append(c.toString())
                }
                i++
            }
        }
    }
    Text(
        text = annotatedMath,
        fontFamily = FontFamily.Serif,
        fontSize = 18.sp,
        color = MaterialTheme.colorScheme.onSurface,
        letterSpacing = 1.sp
    )
}

@Composable
fun InfoAccordionItem(title: String, description: String, formulaContent: @Composable () -> Unit) {
    var expanded by remember { mutableStateOf(false) }
    Column(modifier = Modifier.fillMaxWidth().clickable { expanded = !expanded }.padding(vertical = 12.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
            Text(title, fontFamily = FontFamily.Monospace, fontWeight = FontWeight.Bold, fontSize = 16.sp)
            Icon(
                imageVector = if (expanded) Icons.Default.ExpandLess else Icons.Default.ExpandMore, 
                contentDescription = null, 
                tint = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)
            )
        }
        if (expanded) {
            Column(modifier = Modifier.padding(top = 8.dp)) {
                Text(description, fontSize = 14.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Spacer(Modifier.height(12.dp))
                
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(8.dp))
                        .background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.4f))
                        .padding(16.dp),
                    contentAlignment = Alignment.Center
                ) {
                    formulaContent()
                }
                Spacer(Modifier.height(4.dp))
            }
        }
    }
    HorizontalDivider(color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f))
}"""

content = content.replace(old_content, new_content)

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'w') as f:
    f.write(content)
