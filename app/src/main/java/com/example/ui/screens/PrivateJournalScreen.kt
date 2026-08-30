package com.example.ui.screens

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.TextRange
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.drawText
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.text.rememberTextMeasurer
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Visibility
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.FormatBold
import androidx.compose.material.icons.filled.FormatItalic
import androidx.compose.material.icons.filled.StrikethroughS
import androidx.compose.material.icons.filled.FormatListBulleted
import androidx.compose.material.icons.filled.FormatListNumbered
import androidx.compose.material.icons.filled.Share

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import androidx.fragment.app.FragmentActivity
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.data.JournalEntry
import com.example.data.JournalTemplate
import com.example.viewmodel.MainViewModel
import com.example.viewmodel.UiState
import kotlinx.coroutines.delay
import java.text.SimpleDateFormat
import java.util.*
import androidx.biometric.BiometricPrompt

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PrivateJournalScreen(viewModel: MainViewModel, uiState: UiState, onMenuClick: () -> Unit) {
    var isUnlocked by rememberSaveable { mutableStateOf(false) }

    if (!isUnlocked && uiState.privateJournalLockEnabled) {
        JournalLockScreen(
            uiState = uiState,
            onUnlock = { isUnlocked = true },
            onMenuClick = onMenuClick
        )
    } else {
        JournalMainView(
            viewModel = viewModel,
            uiState = uiState,
            onMenuClick = onMenuClick
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun JournalLockScreen(uiState: UiState, onUnlock: () -> Unit, onMenuClick: () -> Unit) {
    val context = LocalContext.current
    var showPinDialog by remember { mutableStateOf(false) }
    var pin by remember { mutableStateOf("") } // it is actually password
    
    val showBiometrics = remember {
        val fragmentActivity = context as? FragmentActivity
        fragmentActivity != null
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Private Journal") },
                navigationIcon = {
                    IconButton(onClick = onMenuClick) {
                        Icon(Icons.Default.Menu, contentDescription = "Menu")
                    }
                }
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(32.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Icon(
                Icons.Default.Lock,
                contentDescription = "Locked",
                modifier = Modifier.size(64.dp),
                tint = MaterialTheme.colorScheme.primary
            )
            Spacer(modifier = Modifier.height(24.dp))
            Text(
                text = "Journal is Locked",
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(16.dp))
            Text(
                text = "Authenticate to access your private entries.",
                style = MaterialTheme.typography.bodyLarge,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                textAlign = androidx.compose.ui.text.style.TextAlign.Center
            )
            Spacer(modifier = Modifier.height(48.dp))
            
            Button(
                onClick = {
                    val fragmentActivity = context as? FragmentActivity
                    if (fragmentActivity != null) {
                        val executor = ContextCompat.getMainExecutor(context)
                        val biometricPrompt = BiometricPrompt(fragmentActivity, executor,
                            object : BiometricPrompt.AuthenticationCallback() {
                                override fun onAuthenticationError(errorCode: Int, errString: CharSequence) {
                                    super.onAuthenticationError(errorCode, errString)
                                    showPinDialog = true
                                }
                                override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
                                    super.onAuthenticationSucceeded(result)
                                    onUnlock()
                                }
                            })

                        val promptInfo = BiometricPrompt.PromptInfo.Builder()
                            .setTitle("Unlock Private Journal")
                            .setSubtitle("Use your fingerprint or face to unlock")
                            .setNegativeButtonText("Use Password")
                            .build()

                        biometricPrompt.authenticate(promptInfo)
                    } else {
                        showPinDialog = true
                    }
                },
                modifier = Modifier.fillMaxWidth().height(56.dp)
            ) {
                Text("Unlock")
            }
        }
    }
    
    if (showPinDialog) {
        AlertDialog(
            onDismissRequest = { showPinDialog = false },
            title = { Text("Enter Password") },
            text = {
                OutlinedTextField(
                    value = pin,
                    onValueChange = { pin = it },
                    singleLine = true,
                    label = { Text("Password") }
                )
            },
            confirmButton = {
                TextButton(onClick = {
                    if (uiState.appPassword.isBlank() || pin == uiState.appPassword) {
                        onUnlock()
                        showPinDialog = false
                    } else {
                        android.widget.Toast.makeText(context, "Incorrect Password", android.widget.Toast.LENGTH_SHORT).show()
                    }
                }) { Text("Unlock") }
            },
            dismissButton = {
                TextButton(onClick = { showPinDialog = false }) { Text("Cancel") }
            }
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun JournalMainView(
    viewModel: MainViewModel,
    uiState: UiState,
    onMenuClick: () -> Unit
) {
    val entries by viewModel.journalEntries.collectAsStateWithLifecycle(initialValue = emptyList())
    val templates by viewModel.journalTemplates.collectAsStateWithLifecycle(initialValue = emptyList())

    var editingEntry by remember { mutableStateOf<JournalEntry?>(null) }
    var showTemplateSelectionSheet by remember { mutableStateOf(false) }
    var isManagingTemplates by remember { mutableStateOf(false) }

    if (isManagingTemplates) {
        JournalTemplateManagementScreen(
            viewModel = viewModel,
            onClose = { isManagingTemplates = false }
        )
    } else if (editingEntry != null) {
        JournalEditorScreen(
            viewModel = viewModel,
            initialEntry = editingEntry,
            onClose = {
                editingEntry = null
            }
        )
    } else {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text("Private Journal") },
                    navigationIcon = {
                        IconButton(onClick = onMenuClick) {
                            Icon(Icons.Default.Menu, contentDescription = "Menu")
                        }
                    },
                    actions = {
                        IconButton(onClick = { isManagingTemplates = true }) {
                            Icon(Icons.Default.Settings, contentDescription = "Manage Templates")
                        }
                    }
                )
            },
            floatingActionButton = {
                FloatingActionButton(onClick = { showTemplateSelectionSheet = true }, containerColor = MaterialTheme.colorScheme.primary, contentColor = MaterialTheme.colorScheme.background) {
                    Icon(Icons.Default.Add, contentDescription = "New Entry")
                }
            }
        ) { paddingValues ->
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                items(entries, key = { it.entryId }) { entry ->
                    JournalEntryCard(
                        entry = entry,
                        use24HourFormat = uiState.use24HourFormat,
                        onClick = { editingEntry = entry }
                    )
                }
            }
        }
        
        if (showTemplateSelectionSheet) {
            ModalBottomSheet(onDismissRequest = { showTemplateSelectionSheet = false }) {
                Column(modifier = Modifier.padding(bottom = 32.dp)) {
                    Text(
                        text = "New Entry",
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold,
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                    )
                    
                    ListItem(
                        headlineContent = { Text("Blank Entry") },
                        modifier = Modifier.clickable {
                            showTemplateSelectionSheet = false
                            editingEntry = JournalEntry()
                        }
                    )
                    
                    if (templates.isNotEmpty()) {
                        HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))
                        Text(
                            text = "Templates",
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold,
                            modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                        )
                        templates.forEach { template ->
                            ListItem(
                                headlineContent = { Text(template.title) },
                                modifier = Modifier.clickable {
                                    showTemplateSelectionSheet = false
                                    editingEntry = JournalEntry(
                                        title = template.title,
                                        content = template.content
                                    )
                                }
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun JournalEntryCard(entry: JournalEntry, use24HourFormat: Boolean, onClick: () -> Unit) {
    val dateFormat = remember { SimpleDateFormat(if (use24HourFormat) "EEEE, MMM d, yyyy • HH:mm" else "EEEE, MMM d, yyyy • h:mm a", Locale.getDefault()) }
    val dateStr = remember(entry.dateMillis) { dateFormat.format(Date(entry.dateMillis)) }
    
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(24.dp))
            .background(MaterialTheme.colorScheme.surfaceVariant)
            .border(1.dp, MaterialTheme.colorScheme.onSurface.copy(alpha=0.05f), RoundedCornerShape(24.dp))
            .clickable { onClick() }
            .padding(24.dp)
    ) {
        Column {
            Text(
                text = dateStr,
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.primary,
                modifier = Modifier.padding(bottom = 8.dp)
            )
            if (entry.title.isNotBlank()) {
                Text(
                    text = entry.title,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurface,
                    modifier = Modifier.padding(bottom = 4.dp)
                )
            }
            Text(
                text = entry.content.ifBlank { "No content..." },
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 3,
                overflow = TextOverflow.Ellipsis
            )
        }
    }
}


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
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
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

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun JournalTemplateManagementScreen(
    viewModel: MainViewModel,
    onClose: () -> Unit
) {
    val templates by viewModel.journalTemplates.collectAsStateWithLifecycle(initialValue = emptyList())
    var creatingTemplate by remember { mutableStateOf(false) }

    if (creatingTemplate) {
        var title by remember { mutableStateOf("") }
        var content by remember { mutableStateOf("") }

        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text("New Template") },
                    navigationIcon = {
                        IconButton(onClick = { creatingTemplate = false }) {
                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                        }
                    },
                    actions = {
                        TextButton(onClick = {
                            if (title.isNotBlank()) {
                                viewModel.insertJournalTemplate(JournalTemplate(title = title, content = content))
                                creatingTemplate = false
                            }
                        }) {
                            Text("Save")
                        }
                    }
                )
            }
        ) { paddingValues ->
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues)
                    .padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                OutlinedTextField(
                    value = title,
                    onValueChange = { title = it },
                    label = { Text("Template Name") },
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = content,
                    onValueChange = { content = it },
                    label = { Text("Template Content") },
                    modifier = Modifier.fillMaxSize()
                )
            }
        }
    } else {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text("Manage Templates") },
                    navigationIcon = {
                        IconButton(onClick = onClose) {
                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                        }
                    }
                )
            },
            floatingActionButton = {
                FloatingActionButton(onClick = { creatingTemplate = true }, containerColor = MaterialTheme.colorScheme.primary, contentColor = MaterialTheme.colorScheme.background) {
                    Icon(Icons.Default.Add, contentDescription = "New Template")
                }
            }
        ) { paddingValues ->
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues),
                contentPadding = PaddingValues(16.dp)
            ) {
                items(templates, key = { it.templateId }) { template ->
                    ListItem(
                        headlineContent = { Text(template.title) },
                        supportingContent = { Text(template.content, maxLines = 1, overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis) },
                        trailingContent = {
                            IconButton(onClick = { viewModel.deleteJournalTemplate(template) }) {
                                Icon(Icons.Default.Delete, contentDescription = "Delete Template")
                            }
                        }
                    )
                }
            }
        }
    }
}
