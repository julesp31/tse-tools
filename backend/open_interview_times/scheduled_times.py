from datetime import datetime
import re


def get_scheduled_list(athena_query):
    list_of_words = athena_query.split()
    starting_word = "scheduled_times"
    scheduled_boolean = False
    scheduled_list_complete = False
    square_bracket_count = 0
    scheduled_list = []

    for word in list_of_words:
        # print(word)

        if starting_word in word:
            scheduled_boolean = True
            continue

        if scheduled_boolean:
            if '[' in word:
                square_bracket_count += 1

            if ']' in word:
                square_bracket_count -= 1

            if square_bracket_count > 0:
                scheduled_list.append(word)
            elif square_bracket_count <= 0:
                scheduled_boolean = False
                scheduled_list_complete = True
                break

        if scheduled_list_complete:
            break

    return get_blocks(scheduled_list)


def get_blocks(busy_list):
    curly_brace_count = 0
    open_curly = '{'
    closed_curly = '}'
    blocks = []
    current_block = []

    for word in busy_list:
        if open_curly in word:
            curly_amount = 0
            for letter in word:
                if open_curly in letter:
                    curly_amount += 1
                if closed_curly in letter:
                    curly_amount -= 1
            curly_brace_count = curly_brace_count + curly_amount

        if closed_curly in word:
            curly_amount = 0
            for letter in word:
                if open_curly in letter:
                    curly_amount += 1
                if closed_curly in letter:
                    curly_amount -= 1
            curly_brace_count = curly_brace_count + curly_amount

        if curly_brace_count <= 0:
            current_block.append(word)
            blocks.append(current_block)
            current_block = []
            continue

        current_block.append(word)

    '''
    iterator = 1
    for block in blocks:
        print(str(iterator) + ' ' + str(block))
        print()
        print()
        iterator += 1
    '''
    return get_scheduled_times(blocks)


def get_scheduled_times(blocks):
    scheduled_times = []
    block_iterator = 0
    for block in blocks:
        block_iterator += 1
        ending_time = ""
        ending_boolean = False
        starting_time = ""

        for word in block:
            word = word.lower()
            word = word.strip("'")

            match = re.match(r'(\d{4}-\d{2}-\d{2}t\d{2}:\d{2})', word)

            if match and not ending_boolean:
                word = match.group(1).replace("t", " ")
                ending_time = word
                ending_boolean = True

            if match and ending_boolean:
                word = match.group(1).replace("t", " ")
                starting_time = word

        scheduled_times.append(f"{starting_time}|{ending_time}")

    # print(f"Scheduled Times: {scheduled_times}")
    return combine_scheduled_times(scheduled_times)


def combine_scheduled_times(scheduled_times):
    if not scheduled_times:
        return []

    # Step 1: Parse and sort the time blocks
    intervals = [parse_range(t) for t in scheduled_times]
    intervals.sort(key=lambda x: x[0])  # Sort by start time

    # Step 2: Merge overlaps
    merged = [intervals[0]]
    for current_start, current_end in intervals[1:]:
        last_start, last_end = merged[-1]
        if current_start <= last_end:  # Overlapping or touching
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            merged.append((current_start, current_end))

    # Step 3: Format back into strings
    return [format_range(s, e) for s, e in merged]

    return scheduled_times


def parse_range(time_str):
    start_str, end_str = time_str.split('|')
    start_dt = datetime.strptime(start_str.strip(), "%Y-%m-%d %H:%M")
    end_dt = datetime.strptime(end_str.strip(), "%Y-%m-%d %H:%M")

    return start_dt, end_dt


def format_range(start_dt, end_dt):
    return f"{start_dt.strftime('%Y-%m-%d %H:%M')}|{end_dt.strftime('%Y-%m-%d %H:%M')}"
