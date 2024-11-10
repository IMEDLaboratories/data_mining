from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import subprocess
from run_all_checkout import parse_results, save_to_excel  # Twoje funkcje

app = Flask(__name__)
CORS(app)  # Dodaj obsługę CORS dla całej aplikacji

@app.route('/run', methods=['POST'])
def run_scripts():
    # Uruchom swoje skrypty
    scripts = ["appointments_database_checkout.py", "flight_database_checkout.py", "trip_database_checkout.py"]
    for script in scripts:
        subprocess.run(["python", script], capture_output=True, text=True)
    
    return jsonify({"message": "Scripts executed successfully"})

@app.route('/results', methods=['GET'])
def get_results():
    # Parsowanie wyników z result.txt
    data = parse_results("result.txt")
    save_to_excel(data, "database_performance_comparison.xlsx")
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
