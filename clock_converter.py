

def time_converter(time):
    boolean_pm = False

    if time > 1200:
        time = time - 1200
        boolean_pm = True

    time = str(time)
    if len(time) == 3:
        time = time[:1] + ':' + time[1:4]
    else:
        if time == '1200':
            time = '12:00'
        else:
            time = time[:2] + ':' + time[1:5]

    if boolean_pm:
        return 'The converted time is: ' + time + ' p.m.'
    else:
        return 'The converted time is: ' + time + ' a.m.'
