from datetime import datetime


def combine_lists(busy_slots, scheduled_slots):
    combined_busy_list = busy_slots + scheduled_slots

    cleaned_list = merge_time_ranges(combined_busy_list)

    return cleaned_list


def merge_time_ranges(combined_busy_list):
    from datetime import datetime

    def parse_range(time_str):
        start_str, end_str = time_str.split('|')
        start_dt = datetime.strptime(start_str.strip(), "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(end_str.strip(), "%Y-%m-%d %H:%M")
        return start_dt, end_dt

    def format_range(start_dt, end_dt):
        return f"{start_dt.strftime('%Y-%m-%d %H:%M')}|{end_dt.strftime('%Y-%m-%d %H:%M')}"

    if not combined_busy_list:
        return []

    intervals = [parse_range(t) for t in combined_busy_list]
    intervals.sort(key=lambda x: x[0])

    merged = [intervals[0]]
    for current_start, current_end in intervals[1:]:
        last_start, last_end = merged[-1]
        if current_start <= last_end:  # overlap or adjacent
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            merged.append((current_start, current_end))

    return [format_range(s, e) for s, e in merged]
