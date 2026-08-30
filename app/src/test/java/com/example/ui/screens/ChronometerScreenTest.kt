package com.example.ui.screens

import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.onNodeWithText
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import org.robolectric.shadows.ShadowLog

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [36])
class ChronometerScreenTest {

    init {
        ShadowLog.stream = System.out
    }

    @get:Rule val composeTestRule = createComposeRule()

    @Test
    fun `test target deadline opens date picker and then time picker`() {
        composeTestRule.setContent {
            CreateChronometerOverlay(
                onDismiss = {},
                onCreate = { _, _, _, _, _, _ -> }
            )
        }

        composeTestRule.waitForIdle()

        // Click the target deadline row
        composeTestRule.onNodeWithTag("target_deadline_row").performClick()
        composeTestRule.waitForIdle()

        // The date picker dialog should appear
        // The date picker has "Cancel" and "Next" buttons (according to our code)
        composeTestRule.onNodeWithText("Next").assertIsDisplayed()
        
        // Click Next to open the Time Picker
        composeTestRule.onNodeWithText("Next").performClick()
        composeTestRule.waitForIdle()

        // The time picker should appear
        // The time picker has "Cancel" and "OK" buttons, and "Select Time" title
        composeTestRule.onNodeWithText("Select Time").assertIsDisplayed()
        composeTestRule.onNodeWithText("OK").assertIsDisplayed()
        
        // Click OK to close it
        composeTestRule.onNodeWithText("OK").performClick()
        composeTestRule.waitForIdle()
        
        // Verify both dialogs are gone and we are back to the main overlay
        composeTestRule.onNodeWithText("TARGET DEADLINE (ABSOLUTE)").assertIsDisplayed()
    }
}
