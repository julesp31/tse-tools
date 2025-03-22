from datetime import datetime

def removing_excess_times(available_oits):
    simplified_oits = []
    available_oits = dict(sorted(available_oits.items(), key=lambda x: x[0]))

    for item in available_oits:
        oit = ""
        start_year = item.year
        start_month = item.month
        start_day = item.day
        start_hour = item.hour
        start_minute = item.minute
        end_year = available_oits[item].year
        end_month = available_oits[item].month
        end_day = available_oits[item].day
        end_hour = available_oits[item].hour
        end_minute = available_oits[item].minute

        if start_year != end_year or start_month != end_month or start_day != end_day:
            pass
        else:
            oit: str = str(start_month) + "-" + str(start_day) + "-" + str(start_year) + " " +\
                str(start_hour) + ":" + str(start_minute) + " -> " + str(end_hour) + ":" + str(end_minute)

        simplified_oits.append(oit)

    print(simplified_oits)


def merge_excess_times(available_oits):
    intervals = sorted(available_oits.items(), key=lambda x: x[0])

    merged = []
    for start, end in intervals:
        if not merged or start > merged[-1][1]:
            merged.append((start, end))
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))

    return {start: end for start, end in merged}