import math

def get_visual_bounds(start_minutes, end_minutes, title, tag):
    duration_minutes = end_minutes - start_minutes
    
    title_len = len(title)
    tag_len = len(tag)
    max_text_len = max(title_len, tag_len * 0.8)
    estimated_width_dp = 44 + (max_text_len * 8)
    visual_minutes = estimated_width_dp / 1.5
    
    align_text_end = duration_minutes < 150 and end_minutes > 22 * 60
    
    if align_text_end:
        visual_start = end_minutes - max(duration_minutes, visual_minutes)
        return (min(start_minutes, visual_start), end_minutes)
    else:
        visual_end = start_minutes + max(duration_minutes, visual_minutes)
        return (start_minutes, max(end_minutes, visual_end))

print(get_visual_bounds(23 * 60, 23 * 60 + 59, "Depart from station Vishakhapatnam", "Travel"))
print(get_visual_bounds(10 * 60, 11 * 60, "Depart from station Vishakhapatnam", "Travel"))
