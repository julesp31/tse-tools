import sys
import os

# Add backend folder to sys path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, render_template, jsonify
# Import backend functions
from backend.free_busy_times import get_busy_list
from backend.oit_slots import get_oit_list
from backend.times_comparer import split_days
from backend.scheduled_times import get_scheduled_list
from backend.printing_oits import merge_excess_times

# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')

# ------------------------------------
# Open Interview Times (OIT) Formatter
# ------------------------------------

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

@app.route("/", methods=["GET"])
@app.route("/oit", methods=["GET"])
def oit_page():
    return render_template("oit/index.html")

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

@app.route("/admin-oit", methods=["GET"])
def admin_oit_page():
    return render_template("admin_oit/index.html")


# -------------------------
# Comma-Separated Formatter
# -------------------------

# @app.route("/comma-formatter", methods=["GET", "POST"])
# def comma_formatter():
#     if request.method == "POST":
#         input_text = request.form.get("input_text", "")
#         formatted = ", ".join(
#             item.strip() for item in input_text.splitlines() if item.strip()
#         )
#         return render_template(
#             "comma_formatter.html",
#             input_text=input_text,
#             formatted_text=formatted
#         )

#     return render_template(
#         "comma_formatter.html",
#         input_text="",
#         formatted_text=""
#     )

# ---------------------
# Run the TSE Tools app
# ---------------------

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)