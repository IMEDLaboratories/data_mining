'''from flask import Flask, request, jsonify
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
'''
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import psycopg2
import psutil
import time

from dotenv import load_dotenv
import os

# Wczytywanie zmiennych środowiskowe z pliku .env

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})
load_dotenv()
# Ustawienia połączenia z bazą danych
DATABASE_CONFIGS = {
    "python_generator_data": {
        'dbname': 'python_generator_data',
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT'),
    },
    "loty": {
        'dbname': 'loty',
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT'),
    },
    "trip_database": {
        'dbname': 'trip_database',
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT'),
    }
}

def connect_to_db(database):
    """Connect to the selected database."""
    config = DATABASE_CONFIGS[database]
    conn = psycopg2.connect(**config)
    return conn

def measure_query_performance(query, database):
    """Executes a query and measures execution time, RAM, and CPU usage."""
    process = psutil.Process()

    ram_before = process.memory_info().rss / (1024 * 1024)  # RAM in MB
    cpu_before = psutil.cpu_percent(interval=None)

    start_time = time.perf_counter()

    with connect_to_db(database) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            cursor.fetchall()  # Fetch results (if necessary)

    end_time = time.perf_counter()

    ram_after = process.memory_info().rss / (1024 * 1024)  # RAM in MB
    cpu_after = psutil.cpu_percent(interval=None)

    execution_time = end_time - start_time
    avg_ram = (ram_before + ram_after) / 2
    max_ram = max(ram_before, ram_after)
    avg_cpu = (cpu_before + cpu_after) / 2
    max_cpu = max(cpu_before, cpu_after)

    return {
        "executionTime": execution_time,
        "avgRam": avg_ram,
        "maxRam": max_ram,
        "avgCpu": avg_cpu,
        "maxCpu": max_cpu,
    }

@app.route('/query', methods=['POST'])
def run_query():
    data = request.get_json()
    database = data.get("database")
    query = data.get("query")

    # Measure query performance
    results = measure_query_performance(query, database)
    return jsonify([results])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
