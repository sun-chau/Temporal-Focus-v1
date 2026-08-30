import androidx.compose.material.icons.Icons

fun main() {
    val methods = Icons.Default::class.java.methods
    methods.filter { it.name.contains("Touch", ignoreCase = true) || it.name.contains("Long", ignoreCase = true) || it.name.contains("Swipe", ignoreCase = true) }.forEach { println(it.name) }
}
