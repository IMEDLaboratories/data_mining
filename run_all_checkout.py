# -*- coding: utf-8 -*-
import subprocess
import os
import sys

import pandas as pd
import re

# Ścieżki do skryptów
scripts = [
    "appointments_database_checkout.py",
    "flight_database_checkout.py",
    "trip_database_checkout.py"
]


def run_script(script_name):
    print(f"I am starting the script execution: {script_name}...")
    result = subprocess.run(["python", script_name], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Script {script_name} completed successfully\n")
    else:
        print(f"An error occurred while executing the script {script_name}.\n")
        print(result.stderr)


def parse_results(file_path):
    parsed_data = []
    current_database = ""
    current_query = ""

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()

            if line.startswith("BAZA"):
                current_database = line.replace("BAZA ", "")

            elif line.startswith("Wyniki dla zapytania:"):
                # Odczytanie zapytania z następnej linii
                current_query = next(file).strip()

            elif "Czas wykonania" in line:
                # Wyodrębnienie czasu wykonania
                execution_time = float(re.search(r"Czas wykonania: ([\d.]+)", line).group(1))

            elif "Średnie zużycie RAM" in line:
                # Wyodrębnienie średniego i maksymalnego RAM-u
                avg_ram, max_ram = map(float, re.findall(r"[\d.]+", line))

            elif "Średnia wydajność CPU" in line:
                # Wyodrębnienie średniego i maksymalnego CPU
                avg_cpu, max_cpu = map(float, re.findall(r"[\d.]+", line))

                # Zapis danych z bieżącego zapytania
                parsed_data.append({
                    "Baza danych": current_database,
                    "Zapytanie": current_query,
                    "Czas wykonania (s)": execution_time,
                    "Średnie zużycie RAM (MB)": avg_ram,
                    "Maksymalne zużycie RAM (MB)": max_ram,
                    "Średnia wydajność CPU (%)": avg_cpu,
                    "Maksymalna wydajność CPU (%)": max_cpu,
                })

    return parsed_data


def save_to_excel(data, output_file):
    """Save parsed data to an Excel file."""
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)
    print(f"Results saved to file {output_file}")


def main():
    # Check if result.txt exist
    if os.path.exists("result.txt"):
        print("File 'result.txt' already exists. Delete it before starting the program")
        sys.exit(1)

    # Run each script
    for script in scripts:
        run_script(script)

    # Parse results from result.txt
    parsed_data = parse_results("result.txt")

    # Save parsed data to Excel
    save_to_excel(parsed_data, "database_performance_comparison.xlsx")


if __name__ == "__main__":
    main()
