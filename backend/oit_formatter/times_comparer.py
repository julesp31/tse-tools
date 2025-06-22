from datetime import datetime

def parse_range(time_str):
    start_str, end_str = time_str.split('|')
    start_dt = datetime.strptime(start_str.strip(), "%Y-%m-%d %H:%M")
    end_dt = datetime.strptime(end_str.strip(), "%Y-%m-%d %H:%M")
    return start_dt, end_dt


def format_range(start_dt, end_dt):
    return f"{start_dt.strftime('%Y-%m-%d %H:%M')}|{end_dt.strftime('%Y-%m-%d %H:%M')}"


def subtract_intervals(interval, busy_intervals):
    """
    Subtract busy_intervals from interval.
    interval: tuple(start_dt, end_dt)
    busy_intervals: list of tuples (start_dt, end_dt)
    Returns a list of intervals (tuples) that are parts of interval not overlapped by busy_intervals.
    """
    free_intervals = [interval]

    for busy_start, busy_end in busy_intervals:
        new_free_intervals = []
        for free_start, free_end in free_intervals:
            # No overlap
            if busy_end <= free_start or busy_start >= free_end:
                new_free_intervals.append((free_start, free_end))
            else:
                # Overlap cases - split free interval if needed

                # Free before busy interval
                if free_start < busy_start:
                    new_free_intervals.append((free_start, min(busy_start, free_end)))

                # Free after busy interval
                if free_end > busy_end:
                    new_free_intervals.append((max(busy_end, free_start), free_end))

        free_intervals = new_free_intervals
        if not free_intervals:
            break

    return free_intervals


def subtract_lists(oit_slots, busy_slots):
    busy_intervals = [parse_range(b) for b in busy_slots]
    busy_intervals.sort(key=lambda x: x[0])

    result = []
    for oit in oit_slots:
        oit_interval = parse_range(oit)
        free_parts = subtract_intervals(oit_interval, busy_intervals)
        for start, end in free_parts:
            if start < end:
                result.append(format_range(start, end))

    return result
