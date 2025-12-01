#!/usr/bin/env python3
"""
Event filtering and label merging configuration for AST audio event detection.

This config allows easy on/off toggle for filtering/merging.
If the model changes, simply disable filtering or update these lists.
"""

# ========================================
# FEATURE FLAGS - Easy on/off toggle
# ========================================
ENABLE_BLACKLIST_FILTER = True
ENABLE_LABEL_MERGE = True


# ========================================
# BLACKLIST - Events to exclude
# ========================================
# Events that are not useful for behavior analysis
BLACKLIST_EVENTS = [
    # Noise
    "White noise",
    "Static",
    "Hum",
    "Background noise",

    # Insects
    "Insect",
    "Cricket",
    "Crickets",

    # Animals
    "Snake",
    "Sheep",

    # Other
    "Arrow",
]


# ========================================
# LABEL MERGE MAP - Combine similar events
# ========================================
# Format: "Original Label" -> "Merged Label"
# Similar events will be combined under the merged label
LABEL_MERGE_MAP = {
    # Clock sounds - merge Tick into Tick-tock
    "Tick": "Tick-tock",

    # Child speech - merge all child-related speech into one category
    "Child speech, kid speaking": "Child speech",
    "Children shouting": "Child speech",
    "Baby cry, infant cry": "Child speech",
    "Babbling": "Child speech",
    "Children playing": "Child speech",
}


def apply_event_filter(events_list):
    """
    Apply blacklist filtering and label merging to event list.

    Args:
        events_list: List of event dicts with 'label' and 'score' keys

    Returns:
        Filtered and merged event list
    """
    if not events_list:
        return []

    filtered_events = []

    for event in events_list:
        label = event.get("label", "")
        score = event.get("score", 0.0)

        # Step 1: Apply blacklist filter
        if ENABLE_BLACKLIST_FILTER and label in BLACKLIST_EVENTS:
            continue

        # Step 2: Apply label merge
        if ENABLE_LABEL_MERGE and label in LABEL_MERGE_MAP:
            label = LABEL_MERGE_MAP[label]

        # Add to filtered list
        filtered_events.append({
            "label": label,
            "score": score
        })

    # Step 3: Merge duplicate labels (after merging, same label might appear multiple times)
    # Combine scores by taking the maximum score for each label
    merged_dict = {}
    for event in filtered_events:
        label = event["label"]
        score = event["score"]

        if label in merged_dict:
            # Keep the higher score
            merged_dict[label] = max(merged_dict[label], score)
        else:
            merged_dict[label] = score

    # Convert back to list format
    result = [
        {"label": label, "score": score}
        for label, score in merged_dict.items()
    ]

    # Sort by score (descending)
    result.sort(key=lambda x: x["score"], reverse=True)

    return result


def get_filter_stats():
    """
    Get current filter configuration stats.

    Returns:
        Dict with filter statistics
    """
    return {
        "blacklist_enabled": ENABLE_BLACKLIST_FILTER,
        "blacklist_count": len(BLACKLIST_EVENTS),
        "label_merge_enabled": ENABLE_LABEL_MERGE,
        "label_merge_count": len(LABEL_MERGE_MAP),
        "blacklist_events": BLACKLIST_EVENTS if ENABLE_BLACKLIST_FILTER else [],
        "merge_rules": LABEL_MERGE_MAP if ENABLE_LABEL_MERGE else {}
    }
