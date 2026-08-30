package com.example

import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onRoot
import com.example.ui.theme.MyApplicationTheme
import com.github.takahirom.roborazzi.RobolectricDeviceQualifiers
import com.github.takahirom.roborazzi.captureRoboImage
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode

@RunWith(RobolectricTestRunner::class)
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@Config(qualifiers = RobolectricDeviceQualifiers.Pixel8, sdk = [36])
class StatCardScreenshotTest {

  @get:Rule val composeTestRule = createComposeRule()

  @Test
  fun stat_card_screenshot() {
    composeTestRule.setContent { MyApplicationTheme { com.example.ui.components.StatCard(title = "Focus Elapsed", value = "120s") } }

    composeTestRule.onRoot().captureRoboImage(filePath = "src/test/screenshots/stat_card.png")
  }
}
