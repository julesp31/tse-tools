from _datetime import datetime
import re


def combine_dict(my_dict):
    slots_list = []
    current_str = ""
    for key, value in my_dict.items():
        current_str = ''.join(key + value)
        slots_list.append(current_str)

    return slots_list

def remove_milliseconds(date_string):
    # This regex ensures the Z is kept after removing milliseconds
    return re.sub(r'\.\d+', '', date_string).rstrip('Z')

def datetime_dict(my_list):
    date_format = '%Y-%m-%dT%H:%M:%S'
    first_time = ""
    second_time = ""
    my_dict = {}

    for element in my_list:
        string_splitter = element.split(",")
        first_time = string_splitter[0].strip("'")
        first_time = remove_milliseconds(first_time)
        second_time = string_splitter[1].strip("'")
        second_time = remove_milliseconds(second_time)

        try:
            first_date_object = datetime.strptime(first_time, date_format)
            second_date_object = datetime.strptime(second_time, date_format)

            my_dict[first_date_object] = second_date_object

        except ValueError as e:
            print(f"Error: {e}")

    return my_dict


def check_overlap(oit_dict, busy_dict):
    '''
    oit_dict = {
        datetime(2024, 6, 4, 8, 0) : datetime(2024, 6, 4, 10, 0),
        datetime(2024, 6, 4, 12, 0) : datetime(2024, 6, 4, 14, 0),
        datetime(2024, 6, 4, 16, 0): datetime(2024, 6, 4, 18, 0),
    }

    busy_dict = {
        datetime(2024, 6, 4, 9, 0): datetime(2024, 6, 4, 11, 0),
        datetime(2024, 6, 4, 14, 0): datetime(2024, 6, 4, 16, 0),
    }
    '''
    dict_to_remove = []
    for start1, end1 in oit_dict.items():
        for start2, end2 in busy_dict.items():
            if start1 < end2 and start2 < end1:
                print(f"Overlap found between ({start1}, {end1}) and ({start2}, {end2})")
                dict_to_remove.append(start1)

    for element in dict_to_remove:
        if oit_dict.__contains__(element):
            oit_dict.pop(element)

    print(oit_dict)


def split_days(oit_slots, busy_slots):
    oit_list = combine_dict(oit_slots)
    busy_list = combine_dict(busy_slots)

    oit_dictionary = datetime_dict(oit_list)
    busy_dictinoary = datetime_dict(busy_list)

    check_overlap(oit_dictionary, busy_dictinoary)

