package com.example

import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.gestures.ScrollableDefaults
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier

@OptIn(ExperimentalFoundationApi::class)
@Composable
fun Test() {
    val state = rememberPagerState(pageCount = { 10 })
    HorizontalPager(
        state = state,
        flingBehavior = ScrollableDefaults.flingBehavior()
    ) {
    }
}
