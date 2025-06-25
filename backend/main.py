import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, request, render_template, jsonify
from backend.open_interview_times.free_busy_times import get_busy_list
from backend.open_interview_times.oit_slots import get_oit_list
from backend.open_interview_times.scheduled_times import get_scheduled_list
from backend.open_interview_times.combining_busy_times import combine_lists
from backend.open_interview_times.times_comparer import subtract_lists
from datetime import datetime
from backend.comma_separated_list.comma_formatter import format_list

app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "..", "static"),
    template_folder=os.path.join(os.path.dirname(__file__), "..", "templates"),
)


def main(athena_query):
    # Get busy, OIT, and scheduled times from the query
    busy_slots = get_busy_list(athena_query)
    oit_slots = get_oit_list(athena_query)
    scheduled_slots = get_scheduled_list(athena_query)

    # Compare and process times
    cleaned_busy_times = combine_lists(busy_slots, scheduled_slots)
    available_oits = subtract_lists(oit_slots, cleaned_busy_times)

    return available_oits

# Shows the same page for the root www.tsetools.com and OITs page URL
@app.route("/", methods=["GET", "POST"])
@app.route("/open-interview-times", methods=["GET", "POST"])
def open_interview_times():
    return render_template("oit/index.html")


# Comma-separated list page URL
@app.route("/comma-separated-list", methods=["GET", "POST"])
def comma_separated_list():
    return render_template("comma/index.html")


# POST that takes Athena payload and returns OITs
@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    input_text = data.get("text", "")

    athena_query = str(input_text)
    printing_times = main(athena_query)

    print("In process():")
    for t in printing_times:
        print(t)

    # Build a list of lines from printing_times, formatting datetime objects as desired.
    lines = []
    for time_range in printing_times:
        if "|" in time_range:
            start_str, end_str = time_range.split("|")
            start_dt = datetime.strptime(start_str.strip(), "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(end_str.strip(), "%Y-%m-%d %H:%M")
            lines.append(
                f"{start_dt.strftime('%Y-%m-%d %H:%M:%S')} -> {end_dt.strftime('%Y-%m-%d %H:%M:%S')}"
            )

    final_output = "\n".join(lines)

    output = {"printing_times": final_output}

    return jsonify(output)


@app.route("/comma", methods=["POST"])
def comma_tool():
    data = request.get_json()
    input_text = data.get("text", "")

    formatted = format_list(input_text)

    return jsonify({"formatted": formatted})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
