package com.example.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import java.util.regex.Pattern

@Composable
fun MarkdownRenderer(modifier: Modifier = Modifier, text: String) {
    val lines = text.split("\n")
    var index = 0

    Column(modifier = modifier.fillMaxWidth()) {
        while (index < lines.size) {
            val line = lines[index]

            if (line.isBlank()) {
                Spacer(modifier = Modifier.height(8.dp))
                index++
                continue
            }

            if (line.trim() == "---") {
                HorizontalDivider(
                    modifier = Modifier.padding(vertical = 16.dp),
                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.2f)
                )
                index++
                continue
            }

            if (line.startsWith("# ")) {
                Text(
                    text = parseInlineMarkdown(line.removePrefix("# ").trim()),
                    style = MaterialTheme.typography.headlineLarge,
                    modifier = Modifier.padding(top = 16.dp, bottom = 8.dp)
                )
                index++
                continue
            }

            if (line.startsWith("## ")) {
                Text(
                    text = parseInlineMarkdown(line.removePrefix("## ").trim()),
                    style = MaterialTheme.typography.headlineMedium,
                    modifier = Modifier.padding(top = 12.dp, bottom = 6.dp)
                )
                index++
                continue
            }

            if (line.startsWith("### ")) {
                Text(
                    text = parseInlineMarkdown(line.removePrefix("### ").trim()),
                    style = MaterialTheme.typography.headlineSmall,
                    modifier = Modifier.padding(top = 8.dp, bottom = 4.dp)
                )
                index++
                continue
            }

            if (line.startsWith("> ")) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 4.dp)
                ) {
                    Box(
                        modifier = Modifier
                            .width(4.dp)
                            .height(IntrinsicSize.Min)
                            .background(MaterialTheme.colorScheme.primary)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = parseInlineMarkdown(line.removePrefix("> ").trim()),
                        style = MaterialTheme.typography.bodyLarge.copy(
                            fontStyle = FontStyle.Italic,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    )
                }
                index++
                continue
            }

            if (line.trim().startsWith("- ") || line.trim().startsWith("* ")) {
                val prefix = if (line.trim().startsWith("- ")) "- " else "* "
                Row(modifier = Modifier.padding(start = 16.dp, top = 2.dp, bottom = 2.dp)) {
                    Text(text = "• ", style = MaterialTheme.typography.bodyLarge)
                    Text(
                        text = parseInlineMarkdown(line.trim().removePrefix(prefix).trim()),
                        style = MaterialTheme.typography.bodyLarge
                    )
                }
                index++
                continue
            }

            val orderedListMatch = Pattern.compile("^\\d+\\.\\s+(.*)").matcher(line.trim())
            if (orderedListMatch.matches()) {
                val number = line.trim().substringBefore(". ")
                Row(modifier = Modifier.padding(start = 16.dp, top = 2.dp, bottom = 2.dp)) {
                    Text(text = "$number. ", style = MaterialTheme.typography.bodyLarge)
                    Text(
                        text = parseInlineMarkdown(orderedListMatch.group(1) ?: ""),
                        style = MaterialTheme.typography.bodyLarge
                    )
                }
                index++
                continue
            }

            // Paragraph
            Text(
                text = parseInlineMarkdown(line),
                style = MaterialTheme.typography.bodyLarge,
                modifier = Modifier.padding(vertical = 2.dp)
            )
            index++
        }
    }
}

fun parseInlineMarkdown(text: String): AnnotatedString {
    return buildAnnotatedString {
        var i = 0
        while (i < text.length) {
            // **bold**
            if (text.startsWith("**", i) && text.indexOf("**", i + 2) != -1) {
                val end = text.indexOf("**", i + 2)
                pushStyle(SpanStyle(fontWeight = FontWeight.Bold))
                append(text.substring(i + 2, end))
                pop()
                i = end + 2
                continue
            }
            
            // *italic*
            if (text.startsWith("*", i) && text.indexOf("*", i + 1) != -1 && (i == 0 || text[i - 1] == ' ' || !text[i - 1].isLetterOrDigit())) {
                val end = text.indexOf("*", i + 1)
                // Also ensure it's not part of **
                if (end > i + 1) {
                    pushStyle(SpanStyle(fontStyle = FontStyle.Italic))
                    append(text.substring(i + 1, end))
                    pop()
                    i = end + 1
                    continue
                }
            }

            // ~~strikethrough~~
            if (text.startsWith("~~", i) && text.indexOf("~~", i + 2) != -1) {
                val end = text.indexOf("~~", i + 2)
                pushStyle(SpanStyle(textDecoration = TextDecoration.LineThrough))
                append(text.substring(i + 2, end))
                pop()
                i = end + 2
                continue
            }

            append(text[i].toString())
            i++
        }
    }
}
