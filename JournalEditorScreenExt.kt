package com.example.ui.screens

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.TextRange
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.drawText
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.text.rememberTextMeasurer
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.JournalEntry
import com.example.viewmodel.MainViewModel
import kotlinx.coroutines.delay

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun JournalEditorScreen(
    viewModel: MainViewModel,
    initialEntry: JournalEntry?,
    onClose: () -> Unit
) {
    var entry by remember { mutableStateOf(initialEntry ?: JournalEntry()) }
    var title by remember { mutableStateOf(entry.title) }
    var textValue by remember { mutableStateOf(TextFieldValue(entry.content)) }
    var isDirty by remember { mutableStateOf(false) }
    
    var hasBeenSaved by remember { mutableStateOf(false) }
    var isEditMode by remember { mutableStateOf(true) }
    var showExportMenu by remember { mutableStateOf(false) }
    
    val context = LocalContext.current
    
    LaunchedEffect(title, textValue.text) {
        if (isDirty) {
            delay(3000)
            val updated = entry.copy(title = title, content = textValue.text)
            if (!hasBeenSaved) {
                viewModel.insertJournalEntry(updated)
                hasBeenSaved = true
            } else {
                viewModel.updateJournalEntry(updated)
            }
            entry = updated
            isDirty = false
        }
    }

    fun performSaveAndClose() {
        if (isDirty || !hasBeenSaved) {
            val updated = entry.copy(title = title, content = textValue.text)
            if (updated.title.isNotBlank() || updated.content.isNotBlank()) {
                if (!hasBeenSaved) {
                    viewModel.insertJournalEntry(updated)
                } else {
                    viewModel.updateJournalEntry(updated)
                }
            }
        }
        onClose()
    }

    val mdExportLauncher = rememberLauncherForActivityResult(ActivityResultContracts.CreateDocument("text/markdown")) { uri ->
        if (uri != null) {
            context.contentResolver.openOutputStream(uri)?.use { outputStream ->
                outputStream.write(textValue.text.toByteArray())
            }
            android.widget.Toast.makeText(context, "Exported as Markdown", android.widget.Toast.LENGTH_SHORT).show()
        }
    }

    val pdfExportLauncher = rememberLauncherForActivityResult(ActivityResultContracts.CreateDocument("application/pdf")) { uri ->
        if (uri != null) {
            try {
                context.contentResolver.openOutputStream(uri)?.use { outputStream ->
                    val htmlText = textValue.text
                        .replace(Regex("\\*\\*(.*?)\\*\\*"), "<b>$1</b>")
                        .replace(Regex("(?<!\\*)\\*(?!\\*)(.*?)(?<!\\*)\\*(?!\\*)"), "<i>$1</i>")
                        .replace(Regex("~~(.*?)~~"), "<strike>$1</strike>")
                        .replace(Regex("(?m)^### (.*?)$"), "<h3>$1</h3>")
                        .replace(Regex("(?m)^## (.*?)$"), "<h2>$1</h2>")
                        .replace(Regex("(?m)^# (.*?)$"), "<h1>$1</h1>")
                        .replace(Regex("(?m)^- (.*?)$"), "• $1")
                        .replace("\n", "<br>")
                    val spanned = android.text.Html.fromHtml(htmlText, android.text.Html.FROM_HTML_MODE_COMPACT)
                    val textPaint = android.text.TextPaint().apply {
                        color = android.graphics.Color.BLACK
                        textSize = 14f
                    }
                    val staticLayout = android.text.StaticLayout.Builder.obtain(spanned, 0, spanned.length, textPaint, 515)
                        .setAlignment(android.text.Layout.Alignment.ALIGN_NORMAL)
                        .setLineSpacing(0f, 1.2f)
                        .setIncludePad(false)
                        .build()
                    val pdfDocument = android.graphics.pdf.PdfDocument()
                    val pageInfo = android.graphics.pdf.PdfDocument.PageInfo.Builder(595, 842, 1).create()
                    val page = pdfDocument.startPage(pageInfo)
                    page.canvas.translate(40f, 40f)
                    staticLayout.draw(page.canvas)
                    pdfDocument.finishPage(page)
                    pdfDocument.writeTo(outputStream)
                    pdfDocument.close()
                    android.widget.Toast.makeText(context, "Exported as PDF", android.widget.Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    fun applyFormat(prefix: String, suffix: String) {
        val selStart = textValue.selection.start
        val selEnd = textValue.selection.end
        if (selStart != selEnd) {
            val min = minOf(selStart, selEnd)
            val max = maxOf(selStart, selEnd)
            val selectedText = textValue.text.substring(min, max)
            val before = textValue.text.substring(0, min)
            val after = textValue.text.substring(max)
            textValue = TextFieldValue(
                text = before + prefix + selectedText + suffix + after,
                selection = TextRange(min + prefix.length, max + prefix.length)
            )
        } else {
            val before = textValue.text.substring(0, selStart)
            val after = textValue.text.substring(selStart)
            textValue = TextFieldValue(
                text = before + prefix + suffix + after,
                selection = TextRange(selStart + prefix.length)
            )
        }
        isDirty = true
    }

    fun applyPrefix(prefix: String) {
        val selStart = textValue.selection.start
        val lineStart = textValue.text.lastIndexOf('\n', selStart - 1).let { if (it == -1) 0 else it + 1 }
        val before = textValue.text.substring(0, lineStart)
        val after = textValue.text.substring(lineStart)
        textValue = TextFieldValue(
            text = before + prefix + after,
            selection = TextRange(textValue.selection.start + prefix.length, textValue.selection.end + prefix.length)
        )
        isDirty = true
    }

    val textMeasurer = rememberTextMeasurer()
    val textStyle = MaterialTheme.typography.bodyLarge.copy(
        lineHeight = 24.sp,
        fontFamily = FontFamily.Monospace,
        color = MaterialTheme.colorScheme.onSurface
    )
    val charWidth = textMeasurer.measure(" ", style = textStyle).size.width
    val tabWidth = charWidth * 4f
    val gutterColor = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)
    var textLayoutResult by remember { mutableStateOf<androidx.compose.ui.text.TextLayoutResult?>(null) }
    var linePositions by remember { mutableStateOf<List<Float>>(emptyList()) }

    Scaffold(
        contentWindowInsets = WindowInsets.ime,
        topBar = {
            TopAppBar(
                title = { },
                navigationIcon = {
                    IconButton(onClick = { performSaveAndClose() }) {
                        Icon(androidx.compose.material.icons.automirrored.filled.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    Box {
                        IconButton(onClick = { showExportMenu = true }) {
                            Icon(Icons.Default.Share, contentDescription = "Export")
                        }
                        DropdownMenu(
                            expanded = showExportMenu,
                            onDismissRequest = { showExportMenu = false }
                        ) {
                            DropdownMenuItem(
                                text = { Text("Export as Markdown (.md)") },
                                onClick = {
                                    showExportMenu = false
                                    mdExportLauncher.launch("journal_entry.md")
                                }
                            )
                            DropdownMenuItem(
                                text = { Text("Export as PDF (.pdf)") },
                                onClick = {
                                    showExportMenu = false
                                    pdfExportLauncher.launch("journal_entry.pdf")
                                }
                            )
                        }
                    }
                    IconButton(onClick = { isEditMode = !isEditMode }) {
                        Icon(
                            imageVector = if (isEditMode) Icons.Default.Visibility else Icons.Default.Edit,
                            contentDescription = if (isEditMode) "Read Mode" else "Edit Mode"
                        )
                    }
                    TextButton(onClick = { performSaveAndClose() }) {
                        Text("Done")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface,
                    navigationIconContentColor = MaterialTheme.colorScheme.onSurface,
                    actionIconContentColor = MaterialTheme.colorScheme.onSurface
                )
            )
        },
        bottomBar = {
            if (isEditMode) {
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    color = MaterialTheme.colorScheme.surfaceVariant,
                    tonalElevation = 4.dp
                ) {
                    Row(
                        modifier = Modifier
                            .padding(horizontal = 8.dp, vertical = 4.dp)
                            .horizontalScroll(rememberScrollState()),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        IconButton(onClick = { applyFormat("**", "**") }) { Icon(Icons.Default.FormatBold, "Bold") }
                        IconButton(onClick = { applyFormat("*", "*") }) { Icon(Icons.Default.FormatItalic, "Italic") }
                        IconButton(onClick = { applyFormat("~~", "~~") }) { Icon(Icons.Default.StrikethroughS, "Strikethrough") }
                        IconButton(onClick = { applyPrefix("- ") }) { Icon(Icons.Default.FormatListBulleted, "Unordered List") }
                        IconButton(onClick = { applyPrefix("1. ") }) { Icon(Icons.Default.FormatListNumbered, "Ordered List") }
                        IconButton(onClick = { applyPrefix("# ") }) { Text("#", fontWeight = FontWeight.Bold, fontSize = 18.sp) }
                        IconButton(onClick = { applyPrefix("## ") }) { Text("##", fontWeight = FontWeight.Bold, fontSize = 18.sp) }
                        IconButton(onClick = { applyPrefix("### ") }) { Text("###", fontWeight = FontWeight.Bold, fontSize = 18.sp) }
                    }
                }
            }
        }
    ) { paddingValues ->
        if (isEditMode) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues)
                    .background(MaterialTheme.colorScheme.surface)
            ) {
                TextField(
                    value = title,
                    onValueChange = { 
                        title = it
                        isDirty = true
                    },
                    placeholder = { Text("Title (Optional)", style = MaterialTheme.typography.headlineMedium) },
                    textStyle = MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.Bold),
                    colors = TextFieldDefaults.colors(
                        focusedContainerColor = Color.Transparent,
                        unfocusedContainerColor = Color.Transparent,
                        focusedIndicatorColor = Color.Transparent,
                        unfocusedIndicatorColor = Color.Transparent,
                        cursorColor = MaterialTheme.colorScheme.primary
                    ),
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp)
                )
                
                Row(modifier = Modifier.fillMaxSize().verticalScroll(rememberScrollState())) {
                    Canvas(modifier = Modifier.width(48.dp).fillMaxHeight()) {
                        linePositions.forEachIndexed { index, top ->
                            drawText(
                                textMeasurer = textMeasurer,
                                text = "${index + 1}",
                                style = textStyle.copy(color = gutterColor),
                                topLeft = Offset(16.dp.toPx(), top)
                            )
                        }
                    }
                    
                    BasicTextField(
                        value = textValue,
                        onValueChange = { newValue ->
                            var finalValue = newValue
                            if (newValue.text.length == textValue.text.length + 1 && newValue.selection.start == textValue.selection.start + 1) {
                                val addedChar = newValue.text[newValue.selection.start - 1]
                                val closing = when (addedChar) {
                                    '(' -> ')'
                                    '[' -> ']'
                                    '{' -> '}'
                                    '"' -> '"'
                                    '`' -> '`'
                                    else -> null
                                }
                                if (closing != null) {
                                    val before = newValue.text.substring(0, newValue.selection.start)
                                    val after = newValue.text.substring(newValue.selection.start)
                                    finalValue = TextFieldValue(
                                        text = before + closing + after,
                                        selection = newValue.selection
                                    )
                                } else if (addedChar == '\n') {
                                    val prevLineStart = newValue.text.lastIndexOf('\n', newValue.selection.start - 2).let { if (it == -1) 0 else it + 1 }
                                    if (newValue.selection.start - 1 >= prevLineStart) {
                                        val prevLine = newValue.text.substring(prevLineStart, newValue.selection.start - 1)
                                        val match = Regex("^(\\s*[-*]\\s+|\\s*\\d+\\.\\s+)").find(prevLine)
                                        if (match != null) {
                                            val prefix = match.value
                                            val before = newValue.text.substring(0, newValue.selection.start)
                                            val after = newValue.text.substring(newValue.selection.start)
                                            finalValue = TextFieldValue(
                                                text = before + prefix + after,
                                                selection = TextRange(newValue.selection.start + prefix.length)
                                            )
                                        }
                                    }
                                }
                            }
                            textValue = finalValue
                            isDirty = true
                        },
                        textStyle = textStyle,
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(end = 24.dp)
                            .drawBehind {
                                val width = size.width
                                var currentX = tabWidth
                                while (currentX < width) {
                                    drawLine(
                                        color = gutterColor.copy(alpha = 0.2f),
                                        start = Offset(currentX, 0f),
                                        end = Offset(currentX, size.height),
                                        strokeWidth = 1f
                                    )
                                    currentX += tabWidth
                                }
                            },
                        onTextLayout = { result ->
                            textLayoutResult = result
                            val logicalLines = textValue.text.split("\n")
                            val positions = mutableListOf<Float>()
                            var characterIndex = 0
                            for (line in logicalLines) {
                                if (characterIndex <= textValue.text.length) {
                                    val visualLine = result.getLineForOffset(characterIndex)
                                    val top = result.getLineTop(visualLine)
                                    positions.add(top)
                                }
                                characterIndex += line.length + 1
                            }
                            linePositions = positions
                        },
                        cursorBrush = androidx.compose.ui.graphics.SolidColor(MaterialTheme.colorScheme.primary)
                    )
                }
            }
        } else {
            androidx.compose.foundation.lazy.LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues)
                    .background(MaterialTheme.colorScheme.surface)
                    .padding(horizontal = 24.dp),
                contentPadding = PaddingValues(vertical = 16.dp)
            ) {
                item {
                    if (title.isNotBlank()) {
                        Text(
                            text = title,
                            style = MaterialTheme.typography.headlineLarge,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface,
                            modifier = Modifier.padding(bottom = 16.dp)
                        )
                    }
                }
                
                item {
                    if (textValue.text.isBlank()) {
                        Text(
                            text = "Nothing written yet.",
                            style = MaterialTheme.typography.bodyLarge,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.fillMaxWidth(),
                            textAlign = androidx.compose.ui.text.style.TextAlign.Center
                        )
                    } else {
                        Text(
                            text = textValue.text,
                            style = MaterialTheme.typography.bodyLarge.copy(
                                lineHeight = 24.sp,
                                fontFamily = FontFamily.Monospace
                            ),
                            color = MaterialTheme.colorScheme.onSurface
                        )
                    }
                }
            }
        }
    }
}
