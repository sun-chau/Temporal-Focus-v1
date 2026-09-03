import androidx.room.Room
import android.content.Context
fun test(context: Context) {
    Room.databaseBuilder(context, com.example.data.AppDatabase::class.java, "db").fallbackToDestructiveMigration(true)
}
