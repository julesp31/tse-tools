from flask import Flask, request, render_template, jsonify
from free_busy_times import get_busy_list  # Import the function for extracting free/busy data
from oit_slots import get_oit_list  # Import the function for extracting OIT slots

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    input_text = data.get("text", "")
    
    athena_query = str(input_text)
    
    free_busy_data = get_busy_list(athena_query)
    oit_slots = get_oit_list(athena_query)
    
    output = {
        "free_busy_data": free_busy_data,
        "oit_slots": oit_slots
    }
    
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)