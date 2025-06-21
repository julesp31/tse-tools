import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, render_template, jsonify
from backend.free_busy_times import get_busy_list
from backend.oit_slots import get_oit_list
from backend.scheduled_times import get_scheduled_list
from backend.combining_busy_times import combine_lists
from backend.times_comparer import subtract_lists
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')

def main(athena_query):
    # Get busy, OIT, and scheduled times from the query
    busy_slots = get_busy_list(athena_query)
    oit_slots = get_oit_list(athena_query)
    scheduled_slots = get_scheduled_list(athena_query)
    
    # Compare and process times
    cleaned_busy_times = combine_lists(busy_slots, scheduled_slots)
    available_oits = subtract_lists(oit_slots, cleaned_busy_times)
    
    # -----------------------------------------------------------
    # WILL DOUBLE CHECK THIS, I REMOVED THESE LINES
    # for start, end in available_oits.items():
    #     print(f"{start} -> {end}")
    
    # return printing_times
    # -----------------------------------------------------------

    # -----------------------------------------------------------
    # AND I ADDED THESE LINES as available_oits is now a list, not a dictionary.
    # also i don't see printing-times anywhere in the code so it looks like it's not defined
    # Optionally print each available time interval to the console
    # -----------------------------------------------------------

    # -----------------------------------------------------------
    # Added below lines to debug and see output
    for time_range in available_oits:
        print(time_range)

    print("\nBusy Slots:")
    for b in busy_slots:
        print(b)

    print("\nScheduled Slots:")
    for s in scheduled_slots:
        print(s)

    print("\nOIT Slots:")
    for o in oit_slots:
        print(o)

    print("\nCleaned Busy Times:")
    for c in cleaned_busy_times:
        print(c)

    print("\nAvailable OITs:")
    for a in available_oits:
        print(a)

    return available_oits
    # -----------------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    input_text = data.get("text", "")
    
    athena_query = str(input_text)
    printing_times = main(athena_query)

    print("In process():")
    for t in printing_times:
        print(t)
    
    # -------------------------------------------------------------------------------------------------
    # WILL DOUBLE CHECK THIS, I REMOVED THESE LINES AS WELL
    # As available_oits is a list not a dictionary, and we cannot call .items() on it

    # Build a list of lines from printing_times, formatting datetime objects as desired.
    # lines = []
    # for key, value in available_oits.items():
        # If key is a datetime, format it as "YYYY-MM-DD HH:MM:SS"; otherwise, use str()
        # key_str = key.strftime("%Y-%m-%d %H:%M:%S") if hasattr(key, "strftime") else str(key)
        # value_str = value.strftime("%Y-%m-%d %H:%M:%S") if hasattr(value, "strftime") else str(value)
        # lines.append(f"{key_str} -> {value_str}")
    # --------------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------------
    # AND I ADDED THESE LINES
    # Please check this iteration on the start and end times
    lines = []
    for time_range in printing_times:
        if "|" in time_range:
            start_str, end_str = time_range.split("|")
            start_dt = datetime.strptime(start_str.strip(), "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(end_str.strip(), "%Y-%m-%d %H:%M")
            lines.append(f"{start_dt.strftime('%Y-%m-%d %H:%M:%S')} -> {end_dt.strftime('%Y-%m-%d %H:%M:%S')}")
    # --------------------------------------------------------------------------------------------------
    
    final_output = "\n".join(lines)
    
    output = {
        "printing_times": final_output
    }
    
    return jsonify(output)


if __name__ == "__main__":
    app.run(debug=True)
