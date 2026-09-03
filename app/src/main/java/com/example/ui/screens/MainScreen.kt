package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.safeDrawing
import androidx.compose.foundation.layout.only
import androidx.compose.foundation.layout.WindowInsetsSides
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.Image
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.AccessTime
import androidx.compose.material.icons.filled.AccessTime
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.outlined.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.activity.compose.BackHandler
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.viewmodel.TrackerViewModel
import androidx.compose.ui.unit.sp
import androidx.compose.ui.res.vectorResource
import com.example.ui.screens.updateLogs
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import com.example.viewmodel.MainViewModel
import com.example.viewmodel.TimerMode
import com.example.viewmodel.UiState
import com.example.R
import coil.compose.AsyncImage
import coil.request.ImageRequest
import androidx.compose.ui.layout.ContentScale

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainScreen(viewModel: MainViewModel) {
    val uiState by viewModel.uiState.collectAsState()
    val clipboardManager = androidx.compose.ui.platform.LocalClipboardManager.current
    val context = androidx.compose.ui.platform.LocalContext.current
    val drawerState = rememberDrawerState(initialValue = DrawerValue.Closed)
    val scope = rememberCoroutineScope()

    BackHandler(enabled = drawerState.isOpen) {
        scope.launch { drawerState.close() }
    }

    BackHandler(enabled = !drawerState.isOpen && uiState.isCreatingChronometer) {
        viewModel.setEditingTask(null)
        viewModel.setCreatingChronometer(false)
    }

    BackHandler(enabled = !drawerState.isOpen && !uiState.isCreatingChronometer && uiState.currentMode != TimerMode.HOME) {
        if (uiState.currentMode == TimerMode.COLOR_CUSTOMIZATION) {
            viewModel.setTimerMode(TimerMode.SETTINGS)
        } else {
            viewModel.setTimerMode(TimerMode.HOME)
        }
    }

    





    ModalNavigationDrawer(
        drawerState = drawerState,
        gesturesEnabled = drawerState.isOpen,
        drawerContent = {
            ModalDrawerSheet(
                drawerContainerColor = MaterialTheme.colorScheme.surface,
                drawerShape = RoundedCornerShape(topEnd = 16.dp, bottomEnd = 16.dp)
            ) {
                // 1. Rich Drawer Header
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.08f))
                        .padding(24.dp)
                        .clickable {
                            viewModel.setTimerMode(TimerMode.PROFILE)
                            scope.launch { drawerState.close() }
                        }
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        if (uiState.profileImageUri.isNotEmpty()) {
                            Box(
                                modifier = Modifier
                                    .size(72.dp)
                                    .border(1.dp, MaterialTheme.colorScheme.primary, CircleShape)
                                    .padding(6.dp)
                            ) {
                                coil.compose.AsyncImage(
                                    model = coil.request.ImageRequest.Builder(context)
                                        .data(uiState.profileImageUri)
                                        .crossfade(true)
                                        .build(),
                                    contentDescription = "Profile",
                                    contentScale = androidx.compose.ui.layout.ContentScale.Crop,
                                    modifier = Modifier
                                        .fillMaxSize()
                                        .clip(CircleShape)
                                )
                            }
                        } else {
                            Box(
                                modifier = Modifier
                                    .size(72.dp)
                                    .border(1.dp, MaterialTheme.colorScheme.primary, CircleShape)
                                    .padding(6.dp)
                            ) {
                                Box(
                                    modifier = Modifier
                                        .fillMaxSize()
                                        .clip(CircleShape)
                                        .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.2f)),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.Person,
                                        contentDescription = "Profile",
                                        tint = MaterialTheme.colorScheme.primary,
                                        modifier = Modifier.size(36.dp)
                                    )
                                }
                            }
                        }
                        Spacer(modifier = Modifier.width(20.dp))
                        Column {
                            Text(
                                text = "Hi, ${uiState.profileName.takeIf { it.isNotBlank() } ?: "Guest"}",
                                style = MaterialTheme.typography.headlineMedium,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.onSurface,
                                maxLines = 1,
                                overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
                            )
                        }
                    }
                }
                
                HorizontalDivider(color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.05f))

                // Scrollable content
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .verticalScroll(rememberScrollState())
                        .padding(horizontal = 12.dp, vertical = 8.dp)
                ) {
                    // Section 1: Timers
                    // Section 0: Home
                    NavigationDrawerItem(
                        icon = { Icon(Icons.Default.Home, contentDescription = null) },
                        label = { Text("Home") },
                        selected = uiState.currentMode == TimerMode.HOME,
                        onClick = {
                            viewModel.setTimerMode(TimerMode.HOME)
                            scope.launch { drawerState.close() }
                        },
                        shape = RoundedCornerShape(50),
                        colors = NavigationDrawerItemDefaults.colors(
                            selectedContainerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.15f),
                            unselectedContainerColor = Color.Transparent,
                            selectedIconColor = MaterialTheme.colorScheme.primary,
                            selectedTextColor = MaterialTheme.colorScheme.primary,
                            unselectedIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
                            unselectedTextColor = MaterialTheme.colorScheme.onSurfaceVariant
                        ),
                        modifier = Modifier.padding(NavigationDrawerItemDefaults.ItemPadding)
                    )
                    
                    NavigationDrawerItem(
                        icon = { Icon(if (uiState.currentMode == TimerMode.DAILY_SCHEDULE) Icons.Filled.DateRange else Icons.Outlined.DateRange, contentDescription = null) },
                        label = { Text("Daily Schedule") },
                        selected = uiState.currentMode == TimerMode.DAILY_SCHEDULE,
                        onClick = {
                            viewModel.setTimerMode(TimerMode.DAILY_SCHEDULE)
                            scope.launch { drawerState.close() }
                        },
                        shape = RoundedCornerShape(50),
                        colors = NavigationDrawerItemDefaults.colors(
                            selectedContainerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.15f),
                            unselectedContainerColor = Color.Transparent,
                            selectedIconColor = MaterialTheme.colorScheme.primary,
                            selectedTextColor = MaterialTheme.colorScheme.primary,
                            unselectedIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
                            unselectedTextColor = MaterialTheme.colorScheme.onSurfaceVariant
                        ),
                        modifier = Modifier.padding(NavigationDrawerItemDefaults.ItemPadding)
                    )
                    
                    NavigationDrawerItem(
                        icon = { Icon(if (uiState.currentMode == TimerMode.PRIVATE_JOURNAL) Icons.Filled.Book else Icons.Outlined.Book, contentDescription = null) },
                        label = { Text("Private Journal") },
                        selected = uiState.currentMode == TimerMode.PRIVATE_JOURNAL,
                        onClick = {
                            viewModel.setTimerMode(TimerMode.PRIVATE_JOURNAL)
                            scope.launch { drawerState.close() }
                        },
                        shape = RoundedCornerShape(50),
                        colors = NavigationDrawerItemDefaults.colors(
                            selectedContainerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.15f),
                            unselectedContainerColor = Color.Transparent,
                            selectedIconColor = MaterialTheme.colorScheme.primary,
                            selectedTextColor = MaterialTheme.colorScheme.primary,
                            unselectedIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
                            unselectedTextColor = MaterialTheme.colorScheme.onSurfaceVariant
                        ),
                        modifier = Modifier.padding(NavigationDrawerItemDefaults.ItemPadding)
                    )
                    
                    NavigationDrawerItem(
                        icon = { Icon(if (uiState.currentMode == TimerMode.CHECK_INS) Icons.Filled.CheckCircle else Icons.Outlined.CheckCircle, contentDescription = null) },
                        label = { Text("Trackers") },
                        selected = uiState.currentMode == TimerMode.CHECK_INS,
                        onClick = {
                            viewModel.setTimerMode(TimerMode.CHECK_INS)
                            scope.launch { drawerState.close() }
                        },
                        shape = RoundedCornerShape(50),
                        colors = NavigationDrawerItemDefaults.colors(
                            selectedContainerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.15f),
                            unselectedContainerColor = Color.Transparent,
                            selectedIconColor = MaterialTheme.colorScheme.primary,
                            selectedTextColor = MaterialTheme.colorScheme.primary,
                            unselectedIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
                            unselectedTextColor = MaterialTheme.colorScheme.onSurfaceVariant
                        ),
                        modifier = Modifier.padding(NavigationDrawerItemDefaults.ItemPadding)
                    )
                    
                    HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp), color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.05f))
                    
                    NavigationDrawerItem(
                        icon = { Icon(if (uiState.currentMode == TimerMode.CHRONOMETER) Icons.Filled.Timer else Icons.Outlined.Timer, contentDescription = null) },
                        label = { Text("Deadlines") },
                        selected = uiState.currentMode == TimerMode.CHRONOMETER,
                        onClick = {
                            viewModel.setTimerMode(TimerMode.CHRONOMETER)
                            scope.launch { drawerState.close() }
                        },
                        shape = RoundedCornerShape(50),
                        colors = NavigationDrawerItemDefaults.colors(
                            selectedContainerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.15f),
                            unselectedContainerColor = Color.Transparent,
                            selectedIconColor = MaterialTheme.colorScheme.primary,
                            selectedTextColor = MaterialTheme.colorScheme.primary,
                            unselectedIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
                            unselectedTextColor = MaterialTheme.colorScheme.onSurfaceVariant
                        ),
                        modifier = Modifier.padding(NavigationDrawerItemDefaults.ItemPadding)
                    )
                    

                    
                    NavigationDrawerItem(
                        icon = { Icon(if (uiState.currentMode == TimerMode.POMODORO) Icons.Filled.HourglassBottom else Icons.Outlined.HourglassBottom, contentDescription = null) },
                        label = { Text("Pomodoro") },
                        selected = uiState.currentMode == TimerMode.POMODORO,
                        onClick = {
                            viewModel.setTimerMode(TimerMode.POMODORO)
                            scope.launch { drawerState.close() }
                        },
                        shape = RoundedCornerShape(50),
                        colors = NavigationDrawerItemDefaults.colors(
                            selectedContainerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.15f),
                            unselectedContainerColor = Color.Transparent,
                            selectedIconColor = MaterialTheme.colorScheme.primary,
                            selectedTextColor = MaterialTheme.colorScheme.primary,
                            unselectedIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
                            unselectedTextColor = MaterialTheme.colorScheme.onSurfaceVariant
                        ),
                                                modifier = Modifier.padding(NavigationDrawerItemDefaults.ItemPadding)
                    )
                    
                    NavigationDrawerItem(
                        icon = { Icon(if (uiState.currentMode == TimerMode.QUICK_DEADLINES) Icons.Filled.AccessTime else Icons.Outlined.AccessTime, contentDescription = null) },
                        label = { Text("Reminders") },
                        selected = uiState.currentMode == TimerMode.QUICK_DEADLINES,
                        onClick = {
                            viewModel.setTimerMode(TimerMode.QUICK_DEADLINES)
                            scope.launch { drawerState.close() }
                        },
                        shape = RoundedCornerShape(50),
                        colors = NavigationDrawerItemDefaults.colors(
                            selectedContainerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.15f),
                            unselectedContainerColor = Color.Transparent,
                            selectedIconColor = MaterialTheme.colorScheme.primary,
                            selectedTextColor = MaterialTheme.colorScheme.primary,
                            unselectedIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
                            unselectedTextColor = MaterialTheme.colorScheme.onSurfaceVariant
                        ),
                        modifier = Modifier.padding(NavigationDrawerItemDefaults.ItemPadding)
                    )
                    
                    HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp), color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.05f))
                    
                    NavigationDrawerItem(
                        icon = { Icon(if (uiState.currentMode == TimerMode.ANALYTICS) Icons.Filled.BarChart else Icons.Outlined.BarChart, contentDescription = null) },
                        label = { Text("Analytics") },
                        selected = uiState.currentMode == TimerMode.ANALYTICS,
                        onClick = {
                            viewModel.setTimerMode(TimerMode.ANALYTICS)
                            scope.launch { drawerState.close() }
                        },
                        shape = RoundedCornerShape(50),
                        colors = NavigationDrawerItemDefaults.colors(
                            selectedContainerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.15f),
                            unselectedContainerColor = Color.Transparent,
                            selectedIconColor = MaterialTheme.colorScheme.primary,
                            selectedTextColor = MaterialTheme.colorScheme.primary,
                            unselectedIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
                            unselectedTextColor = MaterialTheme.colorScheme.onSurfaceVariant
                        ),
                        modifier = Modifier.padding(NavigationDrawerItemDefaults.ItemPadding)
                    )
                    
                    NavigationDrawerItem(
                        icon = { Icon(if (uiState.currentMode == TimerMode.SETTINGS) Icons.Filled.Settings else Icons.Outlined.Settings, contentDescription = null) },
                        label = { Text("Settings") },
                        selected = uiState.currentMode == TimerMode.SETTINGS,
                        onClick = {
                            viewModel.setTimerMode(TimerMode.SETTINGS)
                            scope.launch { drawerState.close() }
                        },
                        shape = RoundedCornerShape(50),
                        colors = NavigationDrawerItemDefaults.colors(
                            selectedContainerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.15f),
                            unselectedContainerColor = Color.Transparent,
                            selectedIconColor = MaterialTheme.colorScheme.primary,
                            selectedTextColor = MaterialTheme.colorScheme.primary,
                            unselectedIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
                            unselectedTextColor = MaterialTheme.colorScheme.onSurfaceVariant
                        ),
                        modifier = Modifier.padding(NavigationDrawerItemDefaults.ItemPadding)
                    )
                    
                    Spacer(modifier = Modifier.height(24.dp))
                }
            }
        }
    ) {
        Scaffold(
            modifier = Modifier.fillMaxSize(),
            containerColor = MaterialTheme.colorScheme.background,
            contentWindowInsets = if (uiState.currentMode == TimerMode.LANDSCAPE_CHRONOGRAPH) WindowInsets(0, 0, 0, 0) else ScaffoldDefaults.contentWindowInsets
        ) { innerPadding ->
            androidx.compose.animation.Crossfade(
                targetState = uiState.isCreatingChronometer,
                modifier = Modifier.fillMaxSize().padding(if (uiState.currentMode == TimerMode.LANDSCAPE_CHRONOGRAPH) PaddingValues(0.dp) else innerPadding)
            ) { isCreating ->
                if (isCreating) {
                    Box(modifier = Modifier.padding(horizontal = 16.dp)) {
                        CreateChronometerScreen(viewModel)
                    }
                } else {
                    Box(modifier = Modifier.fillMaxSize()) {
                        when (uiState.currentMode) {
                            TimerMode.LANDSCAPE_CHRONOGRAPH -> com.example.ui.screens.LandscapeChronographScreen(
                                viewModel = viewModel,
                                uiState = uiState,
                                onBack = { viewModel.setTimerMode(TimerMode.HOME) }
                            )
                            TimerMode.HOME -> HomeScreen(
                                viewModel = viewModel,
                                uiState = uiState,
                                onMenuClick = { scope.launch { drawerState.open() } },
                                onProfileClick = { viewModel.setTimerMode(TimerMode.PROFILE) }
                            )
                            TimerMode.CHRONOMETER -> ChronometerScreen(viewModel, uiState, onMenuClick = { scope.launch { drawerState.open() } })
                            TimerMode.POMODORO -> PomodoroScreen(viewModel, uiState, onMenuClick = { scope.launch { drawerState.open() } })
                            TimerMode.QUICK_DEADLINES -> QuickDeadlinesScreen(viewModel, uiState, onMenuClick = { scope.launch { drawerState.open() } })
                            TimerMode.DAILY_SCHEDULE -> com.example.ui.screens.DailyScheduleScreen(viewModel, uiState, onMenuClick = { scope.launch { drawerState.open() } })
                            TimerMode.CREATE_DAILY_SCHEDULE -> com.example.ui.screens.CreateDailyScheduleScreen(
                                viewModel = viewModel,
                                uiState = uiState,
                                onBack = { viewModel.setTimerMode(TimerMode.DAILY_SCHEDULE) },
                                onDiscardAndBack = { viewModel.setTimerMode(TimerMode.DAILY_SCHEDULE) }
                            )

                            TimerMode.PROFILE -> UserAccountScreen(viewModel = viewModel, uiState = uiState, onBack = { scope.launch { drawerState.open() } })
                            TimerMode.SETTINGS -> SettingsScreen(viewModel = viewModel, uiState = uiState, onBack = { scope.launch { drawerState.open() } })
                            TimerMode.COLOR_CUSTOMIZATION -> ColorCustomizationScreen(viewModel = viewModel, uiState = uiState, onBack = { viewModel.setTimerMode(TimerMode.SETTINGS) })
                            TimerMode.SECURITY_SETTINGS -> SecuritySettingsScreen(viewModel = viewModel, uiState = uiState, onBack = { viewModel.setTimerMode(TimerMode.SETTINGS) })
                            TimerMode.SETTINGS_APPEARANCE -> SettingsAppearanceScreen(viewModel = viewModel, uiState = uiState, onBack = { viewModel.setTimerMode(TimerMode.SETTINGS) })
                            TimerMode.SETTINGS_LAUNCHER_ICON -> LauncherIconScreen(viewModel = viewModel, uiState = uiState, onBack = { viewModel.setTimerMode(TimerMode.SETTINGS_APPEARANCE) })
                            TimerMode.SETTINGS_FEATURE -> SettingsFeatureScreen(viewModel = viewModel, uiState = uiState, onBack = { viewModel.setTimerMode(TimerMode.SETTINGS) })
                            TimerMode.SETTINGS_DAILY_SCHEDULE -> SettingsDailyScheduleScreen(viewModel = viewModel, uiState = uiState, onBack = { viewModel.setTimerMode(TimerMode.SETTINGS_FEATURE) })
                            TimerMode.SETTINGS_DEADLINES -> SettingsDeadlinesScreen(viewModel = viewModel, uiState = uiState, onBack = { viewModel.setTimerMode(TimerMode.SETTINGS_FEATURE) })
                            TimerMode.SETTINGS_NOTIFICATIONS -> SettingsNotificationsScreen(viewModel = viewModel, uiState = uiState, onBack = { viewModel.setTimerMode(TimerMode.SETTINGS) })
                            TimerMode.SETTINGS_DATA -> SettingsDataScreen(viewModel = viewModel, uiState = uiState, onBack = { viewModel.setTimerMode(TimerMode.SETTINGS) })
                            TimerMode.SETTINGS_SUPPORT -> SettingsSupportScreen(viewModel = viewModel, uiState = uiState, onBack = { viewModel.setTimerMode(TimerMode.SETTINGS) })
                            TimerMode.SETTINGS_ABOUT -> SettingsAboutScreen(onBack = { viewModel.setTimerMode(TimerMode.SETTINGS_SUPPORT) })
                            TimerMode.SETTINGS_HELP -> SettingsHelpScreen(onBack = { viewModel.setTimerMode(TimerMode.SETTINGS_SUPPORT) })
                            TimerMode.SETTINGS_FEEDBACK -> SettingsFeedbackScreen(onBack = { viewModel.setTimerMode(TimerMode.SETTINGS_SUPPORT) })
                            TimerMode.DEVELOPER_OPTIONS -> DeveloperOptionsScreen(onBack = { viewModel.setTimerMode(TimerMode.SETTINGS) })
                            TimerMode.UPDATE_LOG -> UpdateLogScreen(onBack = { scope.launch { drawerState.open() } })
                            TimerMode.ANALYTICS -> AnalyticsDashboardScreen(viewModel = viewModel, uiState = uiState, onBack = { scope.launch { drawerState.open() } }, onOpenProfile = { viewModel.setTimerMode(TimerMode.PROFILE) })
                            TimerMode.PRIVATE_JOURNAL -> PrivateJournalScreen(viewModel = viewModel, uiState = uiState, onMenuClick = { scope.launch { drawerState.open() } })
                            TimerMode.CHECK_INS -> TrackerDashboardScreen(viewModel = viewModel(), onMenuClick = { scope.launch { drawerState.open() } })
                        }
                    }
                }
            }
        }
    }
}



@Composable
fun GlobalHeader(uiState: UiState, onTimeClick: () -> Unit = {}) {
    val date = Date(uiState.currentDateTime)
    val formatter = SimpleDateFormat(if (uiState.use24HourFormat) "EEEE, MMM d | HH:mm:ss" else "EEEE, MMM d | hh:mm:ss a", Locale.getDefault())
    val formattedDate = formatter.format(date)
    
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(12.dp))
            .background(Color.Transparent)
            .clickable { onTimeClick() }
            .padding(vertical = 8.dp, horizontal = 8.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.End
    ) {
        Text(
            text = formattedDate,
            style = MaterialTheme.typography.titleMedium,
            color = MaterialTheme.colorScheme.onSurface,
            fontWeight = FontWeight.Medium,
            fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace
        )
    }
}
