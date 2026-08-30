package com.example.ui.screens

import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.TimePickerState
import org.junit.Test

class TimePickerStateTest {
    @OptIn(ExperimentalMaterial3Api::class)
    @Test
    fun testMethods() {
        val state = TimePickerState(10, 30, true)
        val m = state.javaClass.methods.map { it.name }.joinToString(", ")
        println("METHODS: $m")
    }
}
// force
