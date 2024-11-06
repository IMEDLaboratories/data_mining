import os
import time
import psutil
import psycopg2
from contextlib import contextmanager
from dotenv import load_dotenv

# Wczytywanie zmiennych środowiskowe z pliku .env
load_dotenv()

# Ustawienia połączenia z bazą danych
DATABASE_CONFIG = {
    'dbname': 'przychodnia',
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

@contextmanager
def connect_to_db():
    """Context manager for database connection."""
    conn = psycopg2.connect(**DATABASE_CONFIG)
    try:
        yield conn
    finally:
        conn.close()

def measure_query_performance(query):
    """Executes a query and measures execution time, RAM, and CPU usage efficiently."""

    # Monitorowanie procesu dla RAM i CPU
    process = psutil.Process()

    # Próbka początkowa RAM-u i CPU
    ram_before = process.memory_info().rss / (1024 * 1024)  # RAM in MB
    cpu_before = psutil.cpu_percent(interval=None)

    # Start czasu wykonania zapytania
    start_time = time.perf_counter()

    # Wykonanie zapytania do bazy danych z próbkowaniem RAM i CPU w środku
    with connect_to_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            # Próbka w środku zapytania
            mid_cpu = psutil.cpu_percent(interval=None)
            mid_ram = process.memory_info().rss / (1024 * 1024)  # RAM in MB
            cursor.fetchall()

    # Koniec czasu wykonania zapytania
    end_time = time.perf_counter()

    # Próbka końcowa RAM-u i CPU
    ram_after = process.memory_info().rss / (1024 * 1024)  # RAM in MB
    cpu_after = psutil.cpu_percent(interval=None)

    # Obliczenia wyników
    execution_time = end_time - start_time
    avg_ram = (ram_before + mid_ram + ram_after) / 3
    max_ram = max(ram_before, mid_ram, ram_after)
    avg_cpu = (cpu_before + mid_cpu + cpu_after) / 3
    max_cpu = max(cpu_before, mid_cpu, cpu_after)

    # Przygotowanie wyników do wypisania
    results = (
        f"Wyniki dla zapytania:\n{query}\n"
        f"Czas wykonania: {execution_time:.4f} s\n"
        f"Średnie zużycie RAM: {avg_ram:.4f} MB, Maksymalne zużycie RAM: {max_ram:.4f} MB\n"
        f"Średnia wydajność CPU: {avg_cpu:.4f}%, Maksymalna wydajność CPU: {max_cpu:.4f}%\n"
    )

    # Wyświetlenie wyników na konsoli
    print(results)

    # Zapisanie wyników do pliku
    with open("result.txt", "a") as f:  # 'a' oznacza tryb dopisywania
        f.write(results + "\n")

# Przykładowe zapytania
queries = [
    "SELECT * FROM appointments LIMIT 5;",  # Zwykłe zapytanie 1
    "SELECT d.first_name, d.last_name, COUNT(a.appointment_id) AS total_appointments FROM doctors d JOIN appointments a ON d.doctor_id = a.doctor_id GROUP BY d.first_name, d.last_name;",  # Zwykłe zapytanie 2
    "SELECT first_name, last_name FROM patients WHERE patient_id IN (SELECT patient_id FROM appointments WHERE diagnosis = 'Depression');",  # Zwykłe zapytanie 3
]

def main():
    with open("result.txt", "a") as f:
        f.write("BAZA PRZYCHODNI\n\n")

    print("Start testów dla bazy danych 'przychodnia'...\n")
    for query in queries:
        measure_query_performance(query)

    with open("result.txt", "a") as f:
        f.write("==========\n")
if __name__ == "__main__":
    main()
