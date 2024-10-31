import psycopg2
import time
import os 
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
# Funkcja pomocnicza do łączenia się z bazą, wykonywania zapytań z monitorowaniem
def run_query_with_monitoring(dbname, user, password, host, query, description):
    try:
        # Połączenie z bazą
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        cursor = conn.cursor()
        
        # Uruchamianie monitorowania wydajności zapytania
        print(f"\nUruchamiam zapytanie: {description}")
        start_time = time.time()
        
        # Wykonywanie zapytania z analizą
        cursor.execute(f"EXPLAIN ANALYZE {query}")
        results = cursor.fetchall()
        end_time = time.time()
        
        # Zapisanie wyników monitoringu
        execution_time = end_time - start_time
        print(f"\nWyniki zapytania '{description}':")
        for row in results:
            print(row[0])
        print(f"Czas wykonania (Python): {execution_time:.4f} sekundy")
        
        # Pobieranie informacji z pg_stat_activity
        cursor.execute("SELECT pid, query, state, wait_event, state_change FROM pg_stat_activity WHERE datname = %s;", (dbname,))
        stats = cursor.fetchall()
        print("\nStan procesów podczas zapytania:")
        for stat in stats:
            print(stat)
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Błąd podczas wykonywania zapytania '{description}': {e}")

dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")

# Przykładowe zapytania

# 1. Zapytanie proste
simple_query = "SELECT * FROM appointments LIMIT 5;"

# 2. Zapytanie grupujące z JOIN
grouped_query = '''
SELECT d.first_name, d.last_name, COUNT(a.appointment_id) AS total_appointments
FROM doctors d
JOIN appointments a ON d.doctor_id = a.doctor_id
GROUP BY d.first_name, d.last_name;
'''

# 3. Podzapytanie
subquery = '''
SELECT first_name, last_name
FROM patients
WHERE patient_id IN (SELECT patient_id FROM appointments WHERE diagnosis = 'Depression');
'''

# Wykonanie zapytań z monitorowaniem
run_query_with_monitoring(dbname, user, password, host, simple_query, "Proste zapytanie")
run_query_with_monitoring(dbname, user, password, host, grouped_query, "Zapytanie grupujące (JOIN)")
run_query_with_monitoring(dbname, user, password, host, subquery, "Podzapytanie")
