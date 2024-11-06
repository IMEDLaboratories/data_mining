# -*- coding: utf-8 -*-
import subprocess
import os

# Ścieżki do skryptów
scripts = [
    "appointments_database_checkout.py",
    "flight_database_checkout.py",
    "trip_database_checkout.py"
]

def run_script(script_name):
    print(f"Rozpoczynam wykonywanie skryptu: {script_name}...")
    result = subprocess.run(["python", script_name], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Skrypt {script_name} zakończył się pomyślnie.\n")
    else:
        print(f"Wystąpił błąd podczas wykonywania skryptu {script_name}.\n")
        print(result.stderr)

def main():
    for script in scripts:
        run_script(script)

if __name__ == "__main__":
    main()
