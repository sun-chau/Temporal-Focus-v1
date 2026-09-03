import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.compositeOver

fun main() {
    val a = Color.Red.copy(alpha = 0.5f).compositeOver(Color.White)
}
