package com.example.widget

import android.content.Context
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.glance.Button
import androidx.glance.GlanceId
import androidx.glance.GlanceModifier
import androidx.glance.action.actionStartActivity
import androidx.glance.action.clickable
import androidx.glance.appwidget.GlanceAppWidget
import androidx.glance.appwidget.action.actionRunCallback
import androidx.glance.appwidget.provideContent
import androidx.glance.background
import androidx.glance.layout.Alignment
import androidx.glance.layout.Column
import androidx.glance.layout.Row
import androidx.glance.layout.Spacer
import androidx.glance.layout.fillMaxSize
import androidx.glance.layout.fillMaxWidth
import androidx.glance.layout.height
import androidx.glance.layout.padding
import androidx.glance.text.Text
import androidx.glance.text.TextStyle
import androidx.glance.unit.ColorProvider
import com.example.MainActivity
import com.example.data.AppDatabase
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.runBlocking
import androidx.glance.action.ActionParameters
import androidx.glance.appwidget.action.ActionCallback

class TimerWidget : GlanceAppWidget() {
    override suspend fun provideGlance(context: Context, id: GlanceId) {
        val database = AppDatabase.getDatabase(context)
        val dao = database.timerTaskDao()
        
        provideContent {
            val tasks = runBlocking { dao.getActiveTasks().first() }.take(5)
            
            Column(
                modifier = GlanceModifier
                    .fillMaxSize()
                    .background(ColorProvider(Color(0xFF18181B))) // Midnight Surface
                    .padding(8.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Row(
                    modifier = GlanceModifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        "Temporal Focus",
                        style = TextStyle(color = ColorProvider(Color(0xFFF4F4F5))), // Midnight Base Text
                        modifier = GlanceModifier.defaultWeight()
                    )
                    Button(
                        text = "Refresh",
                        onClick = actionRunCallback<RefreshAction>()
                    )
                }
                Spacer(modifier = GlanceModifier.height(8.dp))
                
                if (tasks.isEmpty()) {
                    Text("No active timers", style = TextStyle(color = ColorProvider(Color(0xFFF4F4F5))))
                } else {
                    Column(modifier = GlanceModifier.fillMaxWidth()) {
                        tasks.forEach { task ->
                            Column(
                                modifier = GlanceModifier
                                    .fillMaxWidth()
                                    .padding(vertical = 4.dp)
                                    .background(ColorProvider(Color(0xFF09090B))) // Midnight Backdrop
                                    .padding(8.dp)
                                    .clickable(actionStartActivity<MainActivity>())
                            ) {
                                Text(task.name, style = TextStyle(color = ColorProvider(Color(0xFFF4F4F5))))
                            }
                        }
                    }
                }
            }
        }
    }
}

class RefreshAction : ActionCallback {
    override suspend fun onAction(
        context: Context,
        glanceId: GlanceId,
        parameters: ActionParameters
    ) {
        TimerWidget().update(context, glanceId)
    }
}
