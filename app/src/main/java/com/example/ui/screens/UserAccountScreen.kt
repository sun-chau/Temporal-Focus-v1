package com.example.ui.screens

import androidx.compose.foundation.BorderStroke
import android.net.Uri
import java.io.File
import java.io.FileOutputStream
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.outlined.*
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Visibility
import androidx.compose.material.icons.filled.PhotoCamera
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Folder
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.example.ui.components.ImageCropperDialog
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.material3.*
import androidx.compose.ui.graphics.Color
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import coil.request.ImageRequest

import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.ui.input.pointer.pointerInput
import com.example.ui.components.ColorPaletteBottomSheet
import com.example.ui.components.STANDARD_PALETTE

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.border
import com.example.viewmodel.MainViewModel
import com.example.viewmodel.UiState
import com.example.ui.utils.getLabelColor
import com.example.ui.utils.getLabelName
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun UserAccountScreen(viewModel: MainViewModel, uiState: UiState, onBack: () -> Unit) {
    var name by remember { mutableStateOf(uiState.profileName) }
    var bio by remember { mutableStateOf(uiState.profileBio) }
    var imageUri by remember { mutableStateOf(uiState.profileImageUri) }
    
    val isDarkTheme = isSystemInDarkTheme()
    val outlineColor = if (isDarkTheme) Color.White.copy(alpha = 0.2f) else Color.Black.copy(alpha = 0.2f)
    val allAvailableColors = remember(uiState.customColors) { STANDARD_PALETTE + uiState.customColors.toList() }
    var newTag by remember { mutableStateOf("") }
    var tagColor by remember { mutableStateOf(allAvailableColors.randomOrNull() ?: "#9E9E9E") }
    var newCategory by remember { mutableStateOf("") }
    var categoryColor by remember { mutableStateOf(allAvailableColors.randomOrNull() ?: "#9E9E9E") }
    
    var showTagColorPalette by remember { mutableStateOf(false) }
    var showCategoryColorPalette by remember { mutableStateOf(false) }

    var showAddFieldDialog by remember { mutableStateOf(false) }
    var showManageFieldsDialog by remember { mutableStateOf(false) }
    var showResetAccountDialog by remember { mutableStateOf(false) }
    var rawSelectedImageUri by remember { mutableStateOf<Uri?>(null) }
    var showProfileMenu by remember { mutableStateOf(false) }
    var viewPhotoUri by remember { mutableStateOf<String?>(null) }
    
    var isSaving by remember { mutableStateOf(false) }
    var isSaved by remember { mutableStateOf(false) }
    val scope = rememberCoroutineScope()
    
    val context = LocalContext.current
    val launcher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        uri?.let {
            try {
                val inputStream = context.contentResolver.openInputStream(it)
                if (inputStream != null) {
                    val file = File(context.filesDir, "raw_profile_pic_${System.currentTimeMillis()}.jpg")
                    val outputStream = FileOutputStream(file)
                    inputStream.copyTo(outputStream)
                    inputStream.close()
                    outputStream.close()
                    rawSelectedImageUri = android.net.Uri.fromFile(file)
                }
            } catch (e: Exception) {
                e.printStackTrace()
                rawSelectedImageUri = it
            }
        }
    }

    if (rawSelectedImageUri != null) {
        ImageCropperDialog(
            uri = rawSelectedImageUri!!,
            onDismiss = { rawSelectedImageUri = null },
            onCropped = { uri -> 
                imageUri = uri.toString()
                rawSelectedImageUri = null
            }
        )
    }

    if (viewPhotoUri != null) {
        Dialog(
            onDismissRequest = { viewPhotoUri = null },
            properties = DialogProperties(usePlatformDefaultWidth = false)
        ) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(MaterialTheme.colorScheme.onSurface)
                    .clickable { viewPhotoUri = null },
                contentAlignment = Alignment.Center
            ) {
                AsyncImage(
                    model = ImageRequest.Builder(LocalContext.current)
                        .data(viewPhotoUri)
                        .crossfade(true)
                        .build(),
                    contentDescription = "Profile Picture Full",
                    contentScale = ContentScale.Fit,
                    modifier = Modifier.fillMaxSize()
                )
            }
        }
    }

    var confirmationStep by remember { mutableStateOf(1) }

    if (showResetAccountDialog) {
        ModalBottomSheet(
            onDismissRequest = { 
                showResetAccountDialog = false 
                confirmationStep = 1
            },
            dragHandle = null,
            shape = androidx.compose.foundation.shape.RoundedCornerShape(topStart = 28.dp, topEnd = 28.dp)
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(24.dp)
            ) {
                if (confirmationStep == 1) {
                    Text(
                        text = "Delete Account (Step 1 of 2)",
                        style = MaterialTheme.typography.headlineSmall,
                        color = MaterialTheme.colorScheme.onSurface,
                        fontWeight = FontWeight.Bold
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(
                        text = "Are you sure you want to delete your account? This will remove all your Categories, Tags, Custom Fields, reset your Name to 'Guest', and clear your Bio.",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Spacer(modifier = Modifier.height(32.dp))
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.End
                    ) {
                        TextButton(onClick = { showResetAccountDialog = false }) {
                            Text("Cancel")
                        }
                        Spacer(modifier = Modifier.width(8.dp))
                        Button(
                            onClick = { confirmationStep = 2 },
                            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)
                        ) {
                            Text("Proceed")
                        }
                    }
                } else {
                    Text(
                        text = "Are you absolutely sure? (Step 2 of 2)",
                        style = MaterialTheme.typography.headlineSmall,
                        color = MaterialTheme.colorScheme.error,
                        fontWeight = FontWeight.Bold
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(
                        text = "This action is final and permanent. All your Categories, Tags, Custom Fields, Name, and Bio will be deleted. This cannot be undone.",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Spacer(modifier = Modifier.height(32.dp))
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.End
                    ) {
                        TextButton(onClick = { confirmationStep = 1 }) {
                            Text("Back")
                        }
                        Spacer(modifier = Modifier.width(8.dp))
                        Button(
                            onClick = {
                                viewModel.deleteAccount()
                                name = "Guest"
                                bio = ""
                                imageUri = ""
                                showResetAccountDialog = false
                                confirmationStep = 1
                                onBack() // Redirect back after deletion
                            },
                            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)
                        ) {
                            Text("Delete Account")
                        }
                    }
                }
            }
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Profile & Labels") },
                navigationIcon = {
                    IconButton(onClick = { onBack() }) {
                        Icon(Icons.Default.Menu, contentDescription = "Menu")
                    }
                },
                actions = {
                    TextButton(onClick = {
                        val hasChanges = name != uiState.profileName || bio != uiState.profileBio || imageUri != uiState.profileImageUri
                        if (hasChanges) {
                            viewModel.updateProfile(name, bio, imageUri)
                            android.widget.Toast.makeText(context, "Changes saved", android.widget.Toast.LENGTH_SHORT).show()
                        } else {
                            android.widget.Toast.makeText(context, "No changes made", android.widget.Toast.LENGTH_SHORT).show()
                        }
                    }) {
                        Text("Save")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.background
                )
            )
        },
        containerColor = MaterialTheme.colorScheme.background
    ) { innerPadding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(24.dp)
        ) {
            item {
                // Profile Image
                Box {
                    Box(
                        modifier = Modifier
                            .size(120.dp)
                            .clip(CircleShape)
                            .background(MaterialTheme.colorScheme.surfaceVariant)
                            .border(2.dp, MaterialTheme.colorScheme.primary, CircleShape)
                            .clickable { showProfileMenu = true },
                        contentAlignment = Alignment.Center
                    ) {
                        if (imageUri.isNotEmpty()) {
                            AsyncImage(
                                model = ImageRequest.Builder(LocalContext.current)
                                    .data(imageUri)
                                    .crossfade(true)
                                    .build(),
                                contentDescription = "Profile Picture",
                                contentScale = ContentScale.Crop,
                                modifier = Modifier.fillMaxSize()
                            )
                        } else {
                            Icon(
                                Icons.Default.Person,
                                contentDescription = "Default Profile",
                                modifier = Modifier.size(64.dp),
                                tint = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                    
                    DropdownMenu(
                        expanded = showProfileMenu,
                        onDismissRequest = { showProfileMenu = false },
                        modifier = Modifier.background(MaterialTheme.colorScheme.surfaceContainerHigh)
                    ) {
                        if (imageUri.isNotEmpty()) {
                            DropdownMenuItem(
                                text = { Text("View photo", color = MaterialTheme.colorScheme.onSurface) },
                                onClick = { 
                                    viewPhotoUri = imageUri
                                    showProfileMenu = false 
                                },
                                leadingIcon = { Icon(Icons.Default.Visibility, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant) }
                            )
                        }
                        DropdownMenuItem(
                            text = { Text("Change/Upload Photo", color = MaterialTheme.colorScheme.onSurface) },
                            onClick = { 
                                launcher.launch("image/*")
                                showProfileMenu = false 
                            },
                            leadingIcon = { Icon(Icons.Default.PhotoCamera, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant) }
                        )
                        if (imageUri.isNotEmpty()) {
                            DropdownMenuItem(
                                text = { Text("Remove photo", color = MaterialTheme.colorScheme.onSurface) },
                                onClick = { 
                                    imageUri = ""
                                    showProfileMenu = false 
                                },
                                leadingIcon = { Icon(Icons.Default.Delete, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant) }
                            )
                        }
                    }
                }
            }

            item {
                // Profile Details
                OutlinedTextField(
                    value = name,
                    onValueChange = { name = it },
                    label = { Text("Name") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true
                )
                Spacer(modifier = Modifier.height(16.dp))
                OutlinedTextField(
                    value = bio,
                    onValueChange = { bio = it },
                    label = { Text("Bio / Additional Info") },
                    modifier = Modifier.fillMaxWidth(),
                    minLines = 3,
                    maxLines = 5
                )
                
                if (uiState.profileCustomFields.isNotEmpty()) {
                    Spacer(modifier = Modifier.height(16.dp))
                    Column(modifier = Modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        uiState.profileCustomFields.forEach { (key, value) ->
                            OutlinedTextField(
                                value = value,
                                onValueChange = {},
                                label = { Text(key) },
                                modifier = Modifier.fillMaxWidth(),
                                readOnly = true
                            )
                        }
                    }
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = { showAddFieldDialog = true }, modifier = Modifier.weight(1f), contentPadding = PaddingValues(vertical = 12.dp)) {
                        Icon(Icons.Default.Input, contentDescription = "Custom Fields", modifier = Modifier.size(24.dp))
                        Spacer(Modifier.width(8.dp))
                        Text("Custom Field", fontSize = 16.sp)
                    }
                    Button(onClick = { showManageFieldsDialog = true }, modifier = Modifier.weight(1f), contentPadding = PaddingValues(vertical = 12.dp)) {
                        Icon(Icons.Default.Badge, contentDescription = "Manage Fields", modifier = Modifier.size(24.dp))
                        Spacer(Modifier.width(8.dp))
                        Text("Manage Fields", fontSize = 16.sp)
                    }
                }
            }

            item {
                HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))
                
                // Tag Manager
                Text(
                    "Tag Manager",
                    style = MaterialTheme.typography.titleMedium,
                    modifier = Modifier.fillMaxWidth()
                )
                Spacer(modifier = Modifier.height(8.dp))
                
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    OutlinedTextField(
                        value = newTag,
                        onValueChange = { newTag = it },
                        label = { Text("New Tag") },
                        modifier = Modifier.weight(1f),
                        singleLine = true,
                        trailingIcon = {
                            Box(
                                modifier = Modifier
                                    .size(24.dp)
                                    .clip(CircleShape)
                                    .background(try { Color(android.graphics.Color.parseColor(tagColor)) } catch(e:Exception){MaterialTheme.colorScheme.onSurfaceVariant})
                                    .border(1.dp, outlineColor, CircleShape)
                                    .pointerInput(Unit) {
                                        detectTapGestures(
                                            onTap = { _ -> tagColor = allAvailableColors.randomOrNull() ?: "#9E9E9E" },
                                            onLongPress = { showTagColorPalette = true }
                                        )
                                    }
                            )
                        }
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Button(onClick = {
                        if (newTag.isNotBlank()) {
                            viewModel.addCustomLabel("${newTag.trim()}|$tagColor")
                            newTag = ""
                            tagColor = allAvailableColors.randomOrNull() ?: "#9E9E9E"
                        }
                    }, contentPadding = PaddingValues(0.dp), modifier = Modifier.size(48.dp).padding(4.dp)) {
                        Icon(Icons.Default.Add, contentDescription = "Add")
                    }
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                
                // Display Tags
                @OptIn(ExperimentalLayoutApi::class)
                FlowRow(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    uiState.customLabels.forEach { tag ->
                        val tagName = getLabelName(tag)
                        val tagColorValue = getLabelColor(tag, uiState.coloredLabelsEnabled)
                        
                        AssistChip(
                            onClick = { },
                            label = { Text(tagName, fontSize = 16.sp, fontWeight = FontWeight.Bold) },
                            modifier = Modifier.height(36.dp),
                            border = BorderStroke(1.dp, if (tagColorValue != Color.Transparent) outlineColor else MaterialTheme.colorScheme.outline),
                            colors = AssistChipDefaults.assistChipColors(
                                labelColor = if (tagColorValue != Color.Transparent) tagColorValue else MaterialTheme.colorScheme.onSurface
                            ),
                            trailingIcon = {
                                IconButton(
                                    onClick = { viewModel.removeCustomLabel(tag) },
                                    modifier = Modifier.size(16.dp)
                                ) {
                                    Icon(
                                        Icons.Default.Close,
                                        contentDescription = "Remove Tag",
                                        modifier = Modifier.size(12.dp),
                                        tint = if (tagColorValue != Color.Transparent) tagColorValue else LocalContentColor.current
                                    )
                                }
                            }
                        )
                    }
                }
            }

            item {
                HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))
                
                // Category Manager
                Text(
                    "Category Manager (Daily Schedule)",
                    style = MaterialTheme.typography.titleMedium,
                    modifier = Modifier.fillMaxWidth()
                )
                Spacer(modifier = Modifier.height(8.dp))
                
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    OutlinedTextField(
                        value = newCategory,
                        onValueChange = { newCategory = it },
                        label = { Text("New Category") },
                        modifier = Modifier.weight(1f),
                        singleLine = true,
                        trailingIcon = {
                            Box(
                                modifier = Modifier
                                    .padding(8.dp)
                                    .size(24.dp)
                                    .clip(androidx.compose.foundation.shape.CircleShape)
                                    .background(try { Color(android.graphics.Color.parseColor(categoryColor)) } catch(e:Exception){MaterialTheme.colorScheme.onSurfaceVariant})
                                    .border(1.dp, outlineColor, androidx.compose.foundation.shape.CircleShape)
                                    .pointerInput(Unit) {
                                        detectTapGestures(
                                            onTap = { _ -> categoryColor = allAvailableColors.randomOrNull() ?: "#9E9E9E" },
                                            onLongPress = { showCategoryColorPalette = true }
                                        )
                                    }
                            )
                        }
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Button(onClick = {
                        if (newCategory.isNotBlank()) {
                            viewModel.addCustomLabel("${newCategory.trim()}|$categoryColor")
                            newCategory = ""
                            categoryColor = allAvailableColors.randomOrNull() ?: "#9E9E9E"
                        }
                    }, contentPadding = PaddingValues(0.dp), modifier = Modifier.size(48.dp).padding(4.dp)) {
                        Icon(Icons.Default.Add, contentDescription = "Add")
                    }
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                
                // Display Categories
                @OptIn(ExperimentalLayoutApi::class)
                FlowRow(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    uiState.customLabels.forEach { category ->
                        val categoryName = getLabelName(category)
                        val categoryColorValue = getLabelColor(category, uiState.coloredLabelsEnabled)
                        
                        AssistChip(
                            onClick = { },
                            label = { Text(categoryName, fontSize = 16.sp, fontWeight = FontWeight.Bold) },
                            modifier = Modifier.height(36.dp),
                            border = BorderStroke(1.dp, if (categoryColorValue != Color.Transparent) outlineColor else MaterialTheme.colorScheme.outline),
                            colors = AssistChipDefaults.assistChipColors(
                                labelColor = if (categoryColorValue != Color.Transparent) categoryColorValue else MaterialTheme.colorScheme.onSurface
                            ),
                            trailingIcon = {
                                IconButton(
                                    onClick = { viewModel.removeCustomLabel(category) },
                                    modifier = Modifier.size(16.dp)
                                ) {
                                    Icon(
                                        Icons.Default.Close,
                                        contentDescription = "Remove Category",
                                        modifier = Modifier.size(12.dp),
                                        tint = if (categoryColorValue != Color.Transparent) categoryColorValue else LocalContentColor.current
                                    )
                                }
                            }
                        )
                    }
                }
            }

            item {
                HorizontalDivider(modifier = Modifier.padding(vertical = 16.dp))
                
                // Data Control
                Button(
                    onClick = { showResetAccountDialog = true },
                    colors = ButtonDefaults.buttonColors(
                        containerColor = MaterialTheme.colorScheme.errorContainer,
                        contentColor = MaterialTheme.colorScheme.onErrorContainer
                    ),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Delete Account")
                }
                Spacer(modifier = Modifier.height(32.dp))
            }
        }
    }

    if (showAddFieldDialog) {
        var fieldName by remember { mutableStateOf("") }
        var fieldValue by remember { mutableStateOf("") }
        ModalBottomSheet(
            onDismissRequest = { showAddFieldDialog = false },
            containerColor = MaterialTheme.colorScheme.surface,
            dragHandle = { BottomSheetDefaults.DragHandle() }
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 24.dp)
                    .padding(bottom = 32.dp)
            ) {
                Text(
                    "Add Custom Field",
                    style = MaterialTheme.typography.headlineSmall,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(bottom = 16.dp)
                )
                OutlinedTextField(
                    value = fieldName,
                    onValueChange = { fieldName = it },
                    label = { Text("Field Name") },
                    modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)
                )
                OutlinedTextField(
                    value = fieldValue,
                    onValueChange = { fieldValue = it },
                    label = { Text("Field Value") },
                    modifier = Modifier.fillMaxWidth().padding(bottom = 24.dp)
                )
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.End
                ) {
                    TextButton(onClick = { showAddFieldDialog = false }) { Text("Cancel") }
                    Spacer(modifier = Modifier.width(8.dp))
                    Button(onClick = { 
                        if (fieldName.isNotBlank() && fieldValue.isNotBlank()) {
                            viewModel.addProfileCustomField(fieldName.trim(), fieldValue.trim())
                            showAddFieldDialog = false
                        }
                    }) { Text("Add") }
                }
            }
        }
    }

    if (showManageFieldsDialog) {
        ModalBottomSheet(
            onDismissRequest = { showManageFieldsDialog = false },
            containerColor = MaterialTheme.colorScheme.surface,
            dragHandle = { BottomSheetDefaults.DragHandle() }
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 24.dp)
                    .padding(bottom = 32.dp)
            ) {
                Text(
                    "Manage Custom Fields",
                    style = MaterialTheme.typography.headlineSmall,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(bottom = 16.dp)
                )
                Column(modifier = Modifier.fillMaxWidth().heightIn(max = 400.dp).verticalScroll(rememberScrollState())) {
                    uiState.profileCustomFields.forEach { (key, value) ->
                        var isEditing by remember { mutableStateOf(false) }
                        if (isEditing) {
                            var editKey by remember { mutableStateOf(key) }
                            var editValue by remember { mutableStateOf(value) }
                            Column(modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)) {
                                OutlinedTextField(value = editKey, onValueChange = { editKey = it }, label = { Text("Field") }, modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp))
                                OutlinedTextField(value = editValue, onValueChange = { editValue = it }, label = { Text("Value") }, modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp))
                                Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.align(Alignment.End)) {
                                    TextButton(onClick = { isEditing = false }) { Text("Cancel") }
                                    Button(onClick = { 
                                        if (editKey.isNotBlank() && editValue.isNotBlank()) {
                                            viewModel.updateProfileCustomField(key, editKey.trim(), editValue.trim())
                                            isEditing = false
                                        }
                                    }) { Text("Save") }
                                }
                            }
                        } else {
                            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 12.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                Column(modifier = Modifier.weight(1f)) {
                                    Text(key, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                                    Spacer(modifier = Modifier.height(4.dp))
                                    Text(value, fontSize = 14.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                }
                                Row {
                                    IconButton(onClick = { isEditing = true }) { Icon(Icons.Outlined.Edit, contentDescription = "Edit", tint = MaterialTheme.colorScheme.primary) }
                                    IconButton(onClick = { viewModel.removeProfileCustomField(key) }) { Icon(Icons.Default.Close, contentDescription = "Delete", tint = MaterialTheme.colorScheme.primary) }
                                }
                            }
                        }
                        HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f))
                    }
                }
                Spacer(modifier = Modifier.height(16.dp))
                Button(onClick = { showManageFieldsDialog = false }, modifier = Modifier.fillMaxWidth()) {
                    Text("Done")
                }
            }
        }
    }

        ColorPaletteBottomSheet(
            isVisible = showTagColorPalette,
            onDismiss = { showTagColorPalette = false },
            selectedColorHex = tagColor,
            customColors = uiState.customColors,
            onColorSelected = { tagColor = it },
            onReset = { tagColor = allAvailableColors.randomOrNull() ?: "#9E9E9E" },
            onAddCustomColor = { viewModel.addCustomColor(it); tagColor = it }
        )

        ColorPaletteBottomSheet(
            isVisible = showCategoryColorPalette,
            onDismiss = { showCategoryColorPalette = false },
            selectedColorHex = categoryColor,
            customColors = uiState.customColors,
            onColorSelected = { categoryColor = it },
            onReset = { categoryColor = allAvailableColors.randomOrNull() ?: "#9E9E9E" },
            onAddCustomColor = { viewModel.addCustomColor(it); categoryColor = it }
        )

}
