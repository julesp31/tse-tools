import re

def format_list(text, delimiter=",", item_prefix="", item_suffix="", result_prefix="", result_suffix="", deduplicate=False):
    items = [item.strip() for item in text.splitlines() if item.strip()]
    if deduplicate:
        seen = set()
        unique_items = []
        for item in items:
            if item not in seen:
                unique_items.append(item)
                seen.add(item)
        items = unique_items

    formatted_items = [f"{item_prefix}{item}{item_suffix}" for item in items]
    return f"{result_prefix}{delimiter.join(formatted_items)}{result_suffix}"