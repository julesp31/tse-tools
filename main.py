from free_busy_times import *
from oit_slots import *
from times_comparer import *


def main():

    # Getting Busy and OIT Times from Athena Query
    print()
    athena_query = str("USER_CALENDAR_LOGGING_QUERY")
    busy_slots = get_busy_list(athena_query)
    print()
    oit_slots = get_oit_list(athena_query)

    split_days(oit_slots, busy_slots)

main()
