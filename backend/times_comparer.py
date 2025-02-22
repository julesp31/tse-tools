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


def merge_busy_dict(busy_dictionary, scheduled_dictionary):
    merged_dictionaries = {}

    '''
    Testing for future improvements -> After merging times it the new busy_time could overlap
    with a time already placed in merged_dictionary -- currently no check
    
    print("Busy Dictionary: ")
    print(busy_dictionary)
    print()

    print("Scheduled Dictionary: ")
    print(scheduled_dictionary)
    print()
    
    scheduled_dictionary = {
        datetime(2024, 6, 4, 8, 0) : datetime(2024, 6, 4, 10, 0),
        datetime(2024, 6, 4, 12, 0) : datetime(2024, 6, 4, 14, 30),
        datetime(2024, 6, 4, 16, 0): datetime(2024, 6, 4, 18, 0),
    }

    busy_dictionary = {
        datetime(2024, 6, 4, 9, 0): datetime(2024, 6, 4, 11, 0),
        datetime(2024, 6, 4, 14, 0): datetime(2024, 6, 4, 16, 00),
    }
    

    for start1, end1 in scheduled_dictionary.items():
        for start2, end2 in busy_dictionary.items():
            if start1 < end2 and start2 < end1:
                # print("Busy Overlapping Times Found Between: " + str(start1) + " -> " + str(scheduled_dictionary[start1])
                      + " and " + str(start2) + " -> " + str(busy_dictionary[start2]))
                start = min(start1, start2)
                print("New Busy Start Time: " + str(start))

                end = max(end1, end2)
                print("New Busy Ending Time: " + str(end))

                merged_dictionaries[start] = end
                print("Added to Merged Dictionary: " + str(start) + " -> " + str(end))
                print()
                # busy_dictionary.pop(start2)
                # scheduled_dictionary.pop(start1)

            merged_dictionaries[start2] = end2
        merged_dictionaries[start1] = end1

    
    for item in merged_dictionaries:
        print(str(item) + " -> " + str(merged_dictionaries[item]))
    print()
    '''

    return merged_dictionaries


'''
def check_overlap(oit_dict, busy_dict):
    oit_dict = {
        datetime(2024, 6, 4, 8, 0) : datetime(2024, 6, 4, 10, 0),
        datetime(2024, 6, 4, 12, 0) : datetime(2024, 6, 4, 14, 0),
        datetime(2024, 6, 4, 16, 0): datetime(2024, 6, 4, 18, 0),
    }

    busy_dict = {
        datetime(2024, 6, 4, 9, 0): datetime(2024, 6, 4, 11, 0),
        datetime(2024, 6, 4, 14, 0): datetime(2024, 6, 4, 16, 0),
    }

    dict_to_remove = []
    for start1, end1 in oit_dict.items():
        for start2, end2 in busy_dict.items():
            if start1 < end2 and start2 < end1:
                # print(f"Overlap found between ({start1}, {end1}) and ({start2}, {end2})")
                dict_to_remove.append(start1)

    for element in dict_to_remove:
        if oit_dict.__contains__(element):
            oit_dict.pop(element)

    return oit_dict
'''


def check_overlapping_oits(oit_dictionary, merged_busy_dictionary):
    available_oits = {}

    '''
    Testing for future improvements -> After merging times it the new busy_time could overlap
    with a time already placed in merged_dictionary -- currently no check

    print("Busy Dictionary: ")
    print(busy_dictionary)
    print()

    print("Scheduled Dictionary: ")
    print(scheduled_dictionary)
    print()
    '''

    oit_dictionary = {
        datetime(2024, 6, 4, 8, 0) : datetime(2024, 6, 4, 10, 0),
        datetime(2024, 6, 4, 12, 0) : datetime(2024, 6, 4, 14, 0),
        datetime(2024, 6, 4, 16, 0): datetime(2024, 6, 4, 18, 0),
    }

    merged_busy_dictionary = {
        datetime(2024, 6, 4, 9, 0): datetime(2024, 6, 4, 11, 0),
        datetime(2024, 6, 4, 14, 0): datetime(2024, 6, 4, 16, 0),
        datetime(2024, 6, 4, 16, 0): datetime(2024, 6, 4, 18, 0),
    }

    for start1, end1 in oit_dictionary.items():
        for start2, end2 in merged_busy_dictionary.items():
            if start1 < end2 and start2 < end1:
                print("OIT Overlapping Times Found Between: " + str(start1) + " -> " + str(oit_dictionary[start1])
                      + " and " + str(start2) + " -> " + str(merged_busy_dictionary[start2]))
                if start1 < start2:
                    start = start1
                    end = start2
                else:
                    start = end2
                    end = end1

                print("New OIT Start Time: " + str(start))
                print("New OIT Ending Time: " + str(end))

                print("Added to Available OITs: " + str(start) + " -> " + str(end))
                print()

                available_oits[start] = end

        # Temporary Solution
        for start in available_oits.keys():
            if start != start1:
                available_oits[start1] = end1

    '''
    for item in available_oits:
        print(str(item) + " -> " + str(available_oits[item]))
    print()
    '''

    return available_oits


def split_days(oit_slots, busy_slots, scheduled_slots):
    oit_list = combine_dict(oit_slots)
    # print("oit List: " + str(oit_list))
    busy_list = combine_dict(busy_slots)
    # print("Busy List: " + str(busy_list))
    scheduled_list = combine_dict(scheduled_slots)
    # print("Scheduled List: " + str(scheduled_slots))

    oit_dictionary = datetime_dict(oit_list)
    busy_dictionary = datetime_dict(busy_list)
    # print("Busy Dictionary Length = " + str(len(busy_dictionary)))
    scheduled_dictionary = datetime_dict(scheduled_list)
    # print("Scheduled Dictionary Length = " + str(len(scheduled_dictionary)))
    merged_busy_dictionary = merge_busy_dict(busy_dictionary, scheduled_dictionary)
    # print("Merged Dictionary Length = " + str(len(merged_dictionaries)))

    oits = check_overlapping_oits(oit_dictionary, merged_busy_dictionary)
    for item in oits:
        print(item, "->", oits[item])

    # print(oit_shit.items())
