from flask import Flask, request, render_template, jsonify
from free_busy_times import get_busy_list
from oit_slots import get_oit_list
from times_comparer import split_days
from scheduled_times import get_scheduled_list
from printing_oits import merge_excess_times

app = Flask(__name__)

def main(athena_query):
    # Get busy, OIT, and scheduled times from the query
    busy_slots = get_busy_list(athena_query)
    oit_slots = get_oit_list(athena_query)
    scheduled_slots = get_scheduled_list(athena_query)
    
    # Compare and process times
    available_oits = split_days(oit_slots, busy_slots, scheduled_slots)
    printing_times = merge_excess_times(available_oits)
    
    # Optionally print each available time interval to the console
    for start, end in printing_times.items():
        print(f"{start} -> {end}")
    
    return printing_times

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    input_text = data.get("text", "")
    
    athena_query = str(input_text)
    printing_times = main(athena_query)
    
    # Build a list of lines from printing_times, formatting datetime objects as desired.
    lines = []
    for key, value in printing_times.items():
        # If key is a datetime, format it as "YYYY-MM-DD HH:MM:SS"; otherwise, use str()
        key_str = key.strftime("%Y-%m-%d %H:%M:%S") if hasattr(key, "strftime") else str(key)
        value_str = value.strftime("%Y-%m-%d %H:%M:%S") if hasattr(value, "strftime") else str(value)
        lines.append(f"{key_str} -> {value_str}")
    
    final_output = "\n".join(lines)
    
    output = {
        "printing_times": final_output
    }
    
    return jsonify(output)


if __name__ == "__main__":
    app.run(debug=True)