import androidx.compose.foundation.gestures.detectHorizontalDragGestures
// This is just a mental check. If I put detectHorizontalDragGestures inside horizontalScroll,
// the inner modifier gets the event first.
// `detectHorizontalDragGestures` consumes the slop unconditionally:
// change.consume() 
// This will prevent the outer `horizontalScroll` from detecting the slop, effectively breaking it!
