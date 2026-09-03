package com.example.data

import androidx.room.TypeConverter

class TrackerConverters {
    @TypeConverter
    fun fromTrackerType(value: TrackerType): String {
        return value.name
    }

    @TypeConverter
    fun toTrackerType(value: String): TrackerType {
        return try {
            TrackerType.valueOf(value)
        } catch (e: Exception) {
            TrackerType.CUSTOM
        }
    }
}
