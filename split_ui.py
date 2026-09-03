import re

with open('app/src/main/java/com/example/ui/screens/TrackerDetailScreen.kt', 'r') as f:
    content = f.read()

def extract_composable(name):
    pattern = r'(@OptIn\([^)]+\)\n)?@Composable\nfun ' + name + r'\(.*?\)\s*{(?:[^{}]*|{(?:[^{}]*|{[^{}]*})*})*}'
    # The above regex might fail on deep nesting. Let's do a simple string index extraction based on "fun <name>".
    start_idx = content.find(f'fun {name}(')
    if start_idx == -1: return ""
    
    # Find the preceding @Composable or @OptIn
    annotations_start = content.rfind('@', 0, start_idx)
    if annotations_start != -1 and 'Composable' in content[annotations_start:start_idx]:
        start_idx = annotations_start
    
    # Find the matching closing brace
    brace_count = 0
    in_string = False
    escape = False
    
    first_brace = content.find('{', start_idx)
    end_idx = first_brace
    
    for i in range(first_brace, len(content)):
        char = content[i]
        if escape:
            escape = False
            continue
        if char == '\\':
            escape = True
            continue
        if char == '"' and not escape:
            in_string = not in_string
            continue
            
        if not in_string:
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_idx = i + 1
                    break
                    
    return content[start_idx:end_idx]

router = extract_composable('TrackerDetailRouter')
gym = extract_composable('GymTrackerUI')
gym_sheet = extract_composable('GymExerciseSheet')
metric_box = extract_composable('MetricBox')
syllabus = extract_composable('SyllabusTrackerUI')
assignment = extract_composable('AssignmentTrackerUI')
custom_main = extract_composable('CustomTrackerUI')
custom_builder = extract_composable('CustomSchemaBuilderUI')
custom_logger = extract_composable('CustomLoggerUI')

header = """package com.example.ui.screens

import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.RectangleShape
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.*
import com.example.viewmodel.TrackerViewModel
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.UUID

"""

with open('app/src/main/java/com/example/ui/screens/TrackerDetailRouter.kt', 'w') as f:
    f.write(header + router)

with open('app/src/main/java/com/example/ui/screens/GymTrackerUI.kt', 'w') as f:
    f.write(header + gym + "\n\n" + gym_sheet + "\n\n" + metric_box)

with open('app/src/main/java/com/example/ui/screens/SyllabusTrackerUI.kt', 'w') as f:
    f.write(header + syllabus)

with open('app/src/main/java/com/example/ui/screens/AssignmentTrackerUI.kt', 'w') as f:
    f.write(header + assignment)

with open('app/src/main/java/com/example/ui/screens/CustomTrackerUI.kt', 'w') as f:
    f.write(header + custom_main + "\n\n" + custom_builder + "\n\n" + custom_logger)

