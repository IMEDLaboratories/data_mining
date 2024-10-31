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

# 1. Proste zapytanie, aby wyświetlić kilka ostatnich wycieczek
simple_query = "SELECT * FROM Trips LIMIT 5;"

# 2. Zapytanie grupujące, aby uzyskać liczbę wycieczek według stacji początkowej
grouped_query = '''
SELECT s.station_name, COUNT(t.trip_id) AS total_trips
FROM Trips t
JOIN Stations s ON t.start_station_id = s.station_id
GROUP BY s.station_name
ORDER BY total_trips DESC;
'''

# 3. Podzapytanie, aby znaleźć użytkowników, którzy odbyli więcej niż 5 wycieczek
subquery = '''
SELECT u.birth_year, u.gender, COUNT(t.trip_id) AS total_trips
FROM Users u
JOIN Trips t ON u.user_id = t.user_id
GROUP BY u.birth_year, u.gender
HAVING COUNT(t.trip_id) > 5;
'''

# Wykonanie zapytań z monitorowaniem
run_query_with_monitoring(dbname, user, password, host, simple_query, "Proste zapytanie")
run_query_with_monitoring(dbname, user, password, host, grouped_query, "Zapytanie grupujące (JOIN)")
run_query_with_monitoring(dbname, user, password, host, subquery, "Podzapytanie")
