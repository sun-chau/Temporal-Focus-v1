package com.example.ui.screens

import android.widget.Toast
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Close

import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Visibility
import androidx.compose.material.icons.filled.VisibilityOff
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import com.example.viewmodel.MainViewModel
import com.example.viewmodel.UiState

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SecuritySettingsScreen(viewModel: MainViewModel, uiState: UiState, onBack: () -> Unit) {
    var privateJournalLockEnabled by remember { mutableStateOf(uiState.privateJournalLockEnabled) }
    var appPasswordEnabled by remember { mutableStateOf(uiState.appPasswordEnabled) }
    var passwordInput by remember { mutableStateOf(uiState.appPassword) }
    var passwordVisible by remember { mutableStateOf(false) }
    var hintInput by remember { mutableStateOf(uiState.passwordHint) }
    var q1 by remember { mutableStateOf(uiState.securityQuestion) }
    var a1 by remember { mutableStateOf(uiState.securityAnswer) }
    var q2 by remember { mutableStateOf(uiState.securityQuestion2) }
    var a2 by remember { mutableStateOf(uiState.securityAnswer2) }
    var q3 by remember { mutableStateOf(uiState.securityQuestion3) }
    var a3 by remember { mutableStateOf(uiState.securityAnswer3) }
    
    val context = LocalContext.current
    
    val canSave = if (appPasswordEnabled) {
        passwordInput.isNotBlank() && 
        q1.isNotBlank() && a1.isNotBlank() &&
        q2.isNotBlank() && a2.isNotBlank() &&
        q3.isNotBlank() && a3.isNotBlank()
    } else {
        true
    }
    
    val scrollState = rememberScrollState()
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Security & Privacy") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        },
        bottomBar = {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                contentAlignment = Alignment.Center
            ) {
                Button(
                    onClick = {
                        viewModel.togglePrivateJournalLock(privateJournalLockEnabled)
                        viewModel.toggleAppPasswordEnabled(appPasswordEnabled)
                        viewModel.setAppPassword(passwordInput)
                        viewModel.setPasswordHint(hintInput)
                        viewModel.setSecurityQuestionsAndAnswers(q1, a1, q2, a2, q3, a3)
                        Toast.makeText(context, "Password saved", Toast.LENGTH_SHORT).show()
                        
                    },
                    enabled = canSave,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Save")
                }
            }
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .verticalScroll(scrollState)
                .padding(16.dp)
        ) {
            ListItem(
                headlineContent = { Text("Private Journal Lock") },
                supportingContent = { Text("Require lock to access private journal") },
                trailingContent = {
                    ThemeSwitch(
                        checked = privateJournalLockEnabled,
                        onCheckedChange = { privateJournalLockEnabled = it }
                    )
                }
            )
            ListItem(
                headlineContent = { Text("Enable App Password") },
                supportingContent = { Text("Require password on launch") },
                trailingContent = {
                    ThemeSwitch(
                        checked = appPasswordEnabled,
                        onCheckedChange = { appPasswordEnabled = it }
                    )
                }
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            OutlinedTextField(
                value = passwordInput,
                onValueChange = { passwordInput = it },
                label = { Text("Password") },
                visualTransformation = if (passwordVisible) VisualTransformation.None else PasswordVisualTransformation(),
                trailingIcon = {
                    val image = if (passwordVisible) Icons.Filled.Visibility else Icons.Filled.VisibilityOff
                    val description = if (passwordVisible) "Hide password" else "Show password"
                    IconButton(onClick = { passwordVisible = !passwordVisible }, enabled = appPasswordEnabled) {
                        Icon(imageVector = image, contentDescription = description)
                    }
                },
                singleLine = true,
                modifier = Modifier.fillMaxWidth(),
                enabled = appPasswordEnabled
            )
            Spacer(Modifier.height(16.dp))
            OutlinedTextField(
                value = hintInput,
                onValueChange = { hintInput = it },
                label = { Text("Password Hint (Optional)") },
                singleLine = true,
                modifier = Modifier.fillMaxWidth(),
                enabled = appPasswordEnabled
            )
            Spacer(Modifier.height(16.dp))
            Text("Security Questions (Required)", style = MaterialTheme.typography.titleMedium, color = if (appPasswordEnabled) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.onSurface.copy(alpha=0.38f))
            Spacer(Modifier.height(8.dp))
            OutlinedTextField(
                value = q1,
                onValueChange = { q1 = it },
                label = { Text("Security Question 1") },
                singleLine = true,
                modifier = Modifier.fillMaxWidth(),
                enabled = appPasswordEnabled
            )
            Spacer(Modifier.height(8.dp))
            OutlinedTextField(
                value = a1,
                onValueChange = { a1 = it },
                label = { Text("Answer 1") },
                singleLine = true,
                modifier = Modifier.fillMaxWidth(),
                enabled = appPasswordEnabled
            )
            Spacer(Modifier.height(16.dp))
            OutlinedTextField(
                value = q2,
                onValueChange = { q2 = it },
                label = { Text("Security Question 2") },
                singleLine = true,
                modifier = Modifier.fillMaxWidth(),
                enabled = appPasswordEnabled
            )
            Spacer(Modifier.height(8.dp))
            OutlinedTextField(
                value = a2,
                onValueChange = { a2 = it },
                label = { Text("Answer 2") },
                singleLine = true,
                modifier = Modifier.fillMaxWidth(),
                enabled = appPasswordEnabled
            )
            Spacer(Modifier.height(16.dp))
            OutlinedTextField(
                value = q3,
                onValueChange = { q3 = it },
                label = { Text("Security Question 3") },
                singleLine = true,
                modifier = Modifier.fillMaxWidth(),
                enabled = appPasswordEnabled
            )
            Spacer(Modifier.height(8.dp))
            OutlinedTextField(
                value = a3,
                onValueChange = { a3 = it },
                label = { Text("Answer 3") },
                singleLine = true,
                modifier = Modifier.fillMaxWidth(),
                enabled = appPasswordEnabled
            )
            Spacer(Modifier.height(32.dp))
        }
    }
}
