from time_to_int import *
from time_zone_converter import *
from clock_converter import *

def main():
    to_utc = False
    print()

    check = input("Please put either 'to utc' or 'to us times': ")
    if 'to utc' in check:
        to_utc = True

    if to_utc:
        us_time = input("What is the US time: ")
        time_zone = input("What tim")
    else:
        utc_time = input("What is the UTC 24 hr time: ")
        converted_time = int_conversion(utc_time)
        time_zone = input("What time zone do you need it converted to: ")
        print()

        time_zone_conversion = to_us_time(time_zone, converted_time)
        clock_conversion = time_converter(time_zone_conversion)
        print(clock_conversion)


main()
