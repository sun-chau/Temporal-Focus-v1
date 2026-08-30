import android.text.SpannableStringBuilder
import android.text.Spanned
import android.text.style.StyleSpan
import android.graphics.Typeface
import android.text.style.StrikethroughSpan
import android.text.style.RelativeSizeSpan

fun renderMarkdown(text: String): Spanned {
    var processed = text
    processed = processed.replace(Regex("\\*\\*(.*?)\\*\\*"), "<b>$1</b>")
    processed = processed.replace(Regex("\\*(.*?)\\*"), "<i>$1</i>")
    processed = processed.replace(Regex("~~(.*?)~~"), "<strike>$1</strike>")
    // headers
    processed = processed.replace(Regex("(?m)^### (.*?)$"), "<h3>$1</h3>")
    processed = processed.replace(Regex("(?m)^## (.*?)$"), "<h2>$1</h2>")
    processed = processed.replace(Regex("(?m)^# (.*?)$"), "<h1>$1</h1>")
    
    return android.text.Html.fromHtml(processed, android.text.Html.FROM_HTML_MODE_COMPACT)
}
