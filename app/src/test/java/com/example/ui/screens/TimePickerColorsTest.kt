package com.example.ui.screens

import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.TimePickerDefaults
import org.junit.Test

class TimePickerColorsTest {
    @OptIn(ExperimentalMaterial3Api::class)
    @Test
    fun testColors() {
        val colors = TimePickerDefaults.colors()
        val m = colors.javaClass.methods.map { it.name }.joinToString(", ")
        println("COLOR_METHODS: $m")
    }
}
