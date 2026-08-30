package com.example.data

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.util.UUID

@Entity(tableName = "journal_entries")
data class JournalEntry(
    @PrimaryKey val entryId: String = UUID.randomUUID().toString(),
    val dateMillis: Long = System.currentTimeMillis(),
    val title: String = "",
    val content: String = "",
    val isPinned: Boolean = false,
    val mood: String = ""
)

@Entity(tableName = "journal_templates")
data class JournalTemplate(
    @PrimaryKey val templateId: String = UUID.randomUUID().toString(),
    val title: String,
    val content: String,
    val isDefault: Boolean = false
)
