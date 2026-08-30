package com.example.ui

import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.TimePickerState
import org.junit.Test

class TimePickerStateTest {
    @OptIn(ExperimentalMaterial3Api::class)
    @Test
    fun testSetters() {
        val state = TimePickerState(10, 30, true)
        val methods = state::class.java.methods.map { it.name }.joinToString(", ")
        println("METHODS_FOUND: $methods")
    }
}
