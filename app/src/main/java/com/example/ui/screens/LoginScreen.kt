package com.example.ui.screens

import android.app.KeyguardManager
import android.content.Context
import android.content.Intent
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.biometric.BiometricManager
import androidx.biometric.BiometricPrompt
import androidx.compose.foundation.Image
import androidx.compose.ui.res.painterResource
import com.example.R
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.LockOpen
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.material.icons.filled.Visibility
import androidx.compose.material.icons.filled.VisibilityOff
import androidx.compose.material.icons.outlined.Visibility
import androidx.compose.material.icons.outlined.VisibilityOff
import androidx.compose.material.icons.automirrored.filled.Login
import androidx.compose.material.icons.filled.Fingerprint

import androidx.compose.ui.unit.dp
import androidx.core.content.ContextCompat
import androidx.fragment.app.FragmentActivity
import coil.compose.AsyncImage
import coil.request.ImageRequest
import com.example.viewmodel.MainViewModel
import com.example.viewmodel.UiState

import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import androidx.compose.ui.platform.LocalLifecycleOwner

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LoginScreen(viewModel: MainViewModel, uiState: UiState) {
    val context = LocalContext.current
    var password by remember { mutableStateOf("") }
    var errorMessage by remember { mutableStateOf("") }
    
    var showHint by remember { mutableStateOf(false) }
    var passwordVisible by remember { mutableStateOf(false) }
    var showForgotPasswordOptions by remember { mutableStateOf(false) }
    var showSecurityQuestionDialog by remember { mutableStateOf(false) }
    var showFactoryResetDialog by remember { mutableStateOf(false) }
    
    val deviceCredentialLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == android.app.Activity.RESULT_OK) {
            viewModel.setAuthenticated(true)
        } else {
            errorMessage = "Device authentication failed"
        }
    }

    val authenticateWithBiometrics = {
        val biometricManager = BiometricManager.from(context)
        if (biometricManager.canAuthenticate(BiometricManager.Authenticators.BIOMETRIC_STRONG or BiometricManager.Authenticators.DEVICE_CREDENTIAL) == BiometricManager.BIOMETRIC_SUCCESS) {
            val executor = ContextCompat.getMainExecutor(context)
            val biometricPrompt = BiometricPrompt(context as FragmentActivity, executor,
                object : BiometricPrompt.AuthenticationCallback() {
                    override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
                        super.onAuthenticationSucceeded(result)
                        viewModel.setAuthenticated(true)
                    }
                    override fun onAuthenticationError(errorCode: Int, errString: CharSequence) {
                        super.onAuthenticationError(errorCode, errString)
                        if (errorCode != BiometricPrompt.ERROR_USER_CANCELED && errorCode != BiometricPrompt.ERROR_NEGATIVE_BUTTON) {
                            errorMessage = errString.toString()
                        }
                    }
                })
            val promptInfo = BiometricPrompt.PromptInfo.Builder()
                .setTitle("Biometric login for Temporal Focus")
                .setSubtitle("Log in using your biometric credential")
                .setAllowedAuthenticators(BiometricManager.Authenticators.BIOMETRIC_STRONG or BiometricManager.Authenticators.DEVICE_CREDENTIAL)
                .build()
            biometricPrompt.authenticate(promptInfo)
        } else {
            errorMessage = "Biometrics not available or not set up"
        }
    }

    // Auto trigger biometric if enabled
    val lifecycleOwner = LocalLifecycleOwner.current
    var hasPromptedThisSession by remember { mutableStateOf(false) }



    Scaffold(
        containerColor = MaterialTheme.colorScheme.background
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(horizontal = 32.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            // Branding Area Slot
            Spacer(modifier = Modifier.height(32.dp))

            // Profile Image
            Box(
                modifier = Modifier
                    .size(128.dp)
                    .border(2.dp, MaterialTheme.colorScheme.primary, CircleShape)
                    .padding(6.dp),
                contentAlignment = Alignment.Center
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .clip(CircleShape)
                        .background(MaterialTheme.colorScheme.surfaceVariant),
                    contentAlignment = Alignment.Center
                ) {
                    if (uiState.profileImageUri.isNotEmpty()) {
                        AsyncImage(
                            model = ImageRequest.Builder(LocalContext.current)
                                .data(uiState.profileImageUri)
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
            }
            Spacer(modifier = Modifier.height(16.dp))
            
            Text(
                text = "Welcome back, ${uiState.profileName}",
                style = MaterialTheme.typography.titleLarge,
                color = MaterialTheme.colorScheme.onBackground
            )

            // Account Switcher Link
            Text(
                text = "Not ${uiState.profileName}? Use another profile",
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.primary,
                modifier = Modifier
                    .padding(top = 8.dp)
                    .clickable { /* future-proofed slot */ }
            )
            
            Spacer(modifier = Modifier.height(32.dp))
            
            val unifiedShape = androidx.compose.foundation.shape.RoundedCornerShape(16.dp)

            OutlinedTextField(
                value = password,
                onValueChange = { 
                    password = it 
                    errorMessage = ""
                },
                label = { Text("Password") },
                visualTransformation = if (passwordVisible) VisualTransformation.None else PasswordVisualTransformation(),
                trailingIcon = {
                    val image = if (passwordVisible) Icons.Outlined.Visibility else Icons.Outlined.VisibilityOff
                    val description = if (passwordVisible) "Hide password" else "Show password"
                    IconButton(onClick = { passwordVisible = !passwordVisible }) {
                        Icon(imageVector = image, contentDescription = description)
                    }
                },
                singleLine = true,
                shape = unifiedShape,
                colors = OutlinedTextFieldDefaults.colors(
                    focusedContainerColor = MaterialTheme.colorScheme.surfaceVariant,
                    unfocusedContainerColor = MaterialTheme.colorScheme.surfaceVariant,
                    focusedBorderColor = MaterialTheme.colorScheme.primary,
                    unfocusedBorderColor = androidx.compose.ui.graphics.Color.Transparent
                ),
                modifier = Modifier.fillMaxWidth()
            )
            
            if (errorMessage.isNotEmpty()) {
                Spacer(modifier = Modifier.height(8.dp))
                Text(text = errorMessage, color = MaterialTheme.colorScheme.error)
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                TextButton(
                    onClick = { showHint = !showHint },
                    contentPadding = PaddingValues(0.dp)
                ) {
                    Text(
                        text = if (showHint) "Hide Hint" else "Show Hint",
                        color = MaterialTheme.colorScheme.primary,
                        style = MaterialTheme.typography.labelLarge
                    )
                }
                TextButton(
                    onClick = { showForgotPasswordOptions = true },
                    contentPadding = PaddingValues(0.dp)
                ) {
                    Text(
                        text = "Forgot Password?",
                        color = MaterialTheme.colorScheme.primary,
                        style = MaterialTheme.typography.labelLarge
                    )
                }
            }
            
            if (showHint) {
                Spacer(modifier = Modifier.height(8.dp))
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(unifiedShape)
                        .background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                        .padding(16.dp)
                ) {
                    if (uiState.passwordHint.isNotEmpty()) {
                        Text(text = "Hint: ${uiState.passwordHint}", style = MaterialTheme.typography.bodyMedium)
                    } else {
                        Text(text = "No hint was set.", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(48.dp)) // Large vertical margin above buttons
            
            Button(
                onClick = {
                    if (password == uiState.appPassword) {
                        viewModel.setAuthenticated(true)
                    } else {
                        errorMessage = "Incorrect password"
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp),
                shape = unifiedShape,
                colors = ButtonDefaults.buttonColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    contentColor = androidx.compose.ui.graphics.Color.White
                )
            ) {
                Icon(Icons.AutoMirrored.Filled.Login, contentDescription = "Login", modifier = Modifier.size(20.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text("Login", style = MaterialTheme.typography.titleMedium)
            }

            Spacer(modifier = Modifier.height(16.dp))
            
            Button(
                onClick = { authenticateWithBiometrics() },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp),
                shape = unifiedShape,
                colors = ButtonDefaults.buttonColors(
                    containerColor = MaterialTheme.colorScheme.surfaceVariant, 
                    contentColor = androidx.compose.ui.graphics.Color(0xFFE0E0E0)
                )
            ) {
                Icon(Icons.Default.Fingerprint, contentDescription = "Biometrics", modifier = Modifier.size(20.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text("Unlock with Biometrics", style = MaterialTheme.typography.titleMedium)
            }
        }
    }


    
    if (showForgotPasswordOptions) {
        ModalBottomSheet(
            onDismissRequest = { showForgotPasswordOptions = false },
            dragHandle = null,
            shape = androidx.compose.foundation.shape.RoundedCornerShape(topStart = 28.dp, topEnd = 28.dp)
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(24.dp)
            ) {
                Text("Recovery Options", style = MaterialTheme.typography.headlineSmall)
                Spacer(modifier = Modifier.height(16.dp))
                

                // 2. Device Unlock Password
                ListItem(
                    headlineContent = { Text("Use Device Password") },
                    supportingContent = { Text("Unlock with your device PIN, pattern, or password") },
                    modifier = Modifier.clickable {
                        showForgotPasswordOptions = false
                        val keyguardManager = context.getSystemService(Context.KEYGUARD_SERVICE) as KeyguardManager
                        if (keyguardManager.isKeyguardSecure) {
                            val intent = keyguardManager.createConfirmDeviceCredentialIntent("Unlock Temporal Focus", "Confirm your device password to log in")
                            if (intent != null) {
                                deviceCredentialLauncher.launch(intent)
                            }
                        } else {
                            errorMessage = "No device security set up"
                        }
                    }
                )
                
                // 3. Security Questions
                if (uiState.securityQuestion.isNotEmpty()) {
                    ListItem(
                        headlineContent = { Text("Answer Security Question") },
                        supportingContent = { Text("Bypass using your configured question") },
                        modifier = Modifier.clickable {
                            showForgotPasswordOptions = false
                            showSecurityQuestionDialog = true
                        }
                    )
                }
                
                // 4. Factory Reset
                ListItem(
                    headlineContent = { Text("Factory Reset", color = MaterialTheme.colorScheme.error) },
                    supportingContent = { Text("Delete all data and reset the app", color = MaterialTheme.colorScheme.error) },
                    modifier = Modifier.clickable {
                        showForgotPasswordOptions = false
                        showFactoryResetDialog = true
                    }
                )
            }
        }
    }
    
    if (showSecurityQuestionDialog) {
        var answer by remember { mutableStateOf("") }
        var answerError by remember { mutableStateOf("") }
        AlertDialog(
            onDismissRequest = { showSecurityQuestionDialog = false },
            title = { Text("Security Question") },
            text = {
                Column {
                    Text(uiState.securityQuestion)
                    Spacer(Modifier.height(16.dp))
                    OutlinedTextField(
                        value = answer,
                        onValueChange = { 
                            answer = it 
                            answerError = ""
                        },
                        label = { Text("Answer") },
                        singleLine = true,
                        modifier = Modifier.fillMaxWidth()
                    )
                    if (answerError.isNotEmpty()) {
                        Text(text = answerError, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall)
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = {
                    if (answer.trim().equals(uiState.securityAnswer.trim(), ignoreCase = true)) {
                        showSecurityQuestionDialog = false
                        viewModel.setAuthenticated(true)
                    } else {
                        answerError = "Incorrect answer"
                    }
                }) {
                    Text("Submit")
                }
            },
            dismissButton = {
                TextButton(onClick = { showSecurityQuestionDialog = false }) {
                    Text("Cancel")
                }
            }
        )
    }
    
    if (showFactoryResetDialog) {
        AlertDialog(
            onDismissRequest = { showFactoryResetDialog = false },
            title = { Text("Factory Reset") },
            text = { Text("This will delete all deadlines, Pomodoro statistics, profile data, custom tags, and reset your app password. This action cannot be undone. Are you sure you want to proceed?") },
            confirmButton = {
                TextButton(onClick = {
                    viewModel.factoryResetUserData()
                    // Reset password explicitly since we are locked out
                    viewModel.toggleAppPasswordEnabled(false)
                    viewModel.setAppPassword("")
                    viewModel.setAuthenticated(true) // let them in after reset
                    showFactoryResetDialog = false
                }) {
                    Text("Reset All Data", color = MaterialTheme.colorScheme.error)
                }
            },
            dismissButton = {
                TextButton(onClick = { showFactoryResetDialog = false }) {
                    Text("Cancel")
                }
            }
        )
    }
}
