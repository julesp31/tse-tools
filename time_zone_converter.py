

def to_us_time(timezone, time):
    if timezone == 'EDT':
        time -= 400
    if timezone == 'EST':
        time -= 500
    if timezone == 'CDT':
        time -= 500
    if timezone == 'CST':
        time -= 600
    if timezone == 'MDT':
        time -= 600
    if timezone == 'MST':
        time -= 700
    if timezone == 'PDT':
        time -= 700
    if timezone == 'PST':
        time -= 800
    if timezone == 'HST':
        time -= 1000

    return time


def to_utc_time(timezone, time):
    if timezone == 'EDT':
        time += 400
    if timezone == 'EST':
        time += 500
    if timezone == 'CDT':
        time += 500
    if timezone == 'CST':
        time += 600
    if timezone == 'MDT':
        time += 600
    if timezone == 'MST':
        time += 700
    if timezone == 'PDT':
        time += 700
    if timezone == 'PST':
        time += 800
    if timezone == 'HST':
        time += 1000

    return time