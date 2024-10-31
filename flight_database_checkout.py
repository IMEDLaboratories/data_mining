import psycopg2
import time
import os 
from dotenv import load_dotenv
from datetime import datetime

# Ładowanie zmiennych środowiskowych
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

# Konfiguracja bazy danych
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")

# Przykładowe zapytania

# 1. Proste zapytanie, aby wyświetlić kilka ostatnich lotów
simple_query = "SELECT * FROM flights LIMIT 5;"

# 2. Zapytanie grupujące, aby uzyskać liczbę lotów według linii lotniczej
grouped_query = '''
SELECT a.airline, COUNT(f.flight_number) AS total_flights
FROM flights f
JOIN airlines a ON f.airline = a.iata_code
GROUP BY a.airline
ORDER BY total_flights DESC;
'''

# 3. Podzapytanie, aby znaleźć lotniska, które mają więcej niż 10 lotów jako lotnisko startowe
subquery = '''
SELECT ap.airport, COUNT(f.flight_number) AS total_departures
FROM airports ap
JOIN flights f ON ap.iata_code = f.origin_airport
GROUP BY ap.airport
HAVING COUNT(f.flight_number) > 10;
'''

# Wykonanie zapytań z monitorowaniem
run_query_with_monitoring(dbname, user, password, host, simple_query, "Proste zapytanie")
run_query_with_monitoring(dbname, user, password, host, grouped_query, "Zapytanie grupujące (JOIN)")
run_query_with_monitoring(dbname, user, password, host, subquery, "Podzapytanie")
