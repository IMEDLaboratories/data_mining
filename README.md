# Database Benchmarking Scripts

This repository contains Python scripts to benchmark SQL query performance on PostgreSQL relational databases for three distinct domains:
1. **Trips** - `trip_database_checkout.py`
2. **Flights** - `flight_database_checkout.py`
3. **Medical Appointments** - `appointments_database_checkout.py`

Each script measures the execution time, CPU, and memory usage for a series of queries to evaluate the efficiency of these databases under different loads. Results can help optimize query performance and resource allocation.

## Project Structure

- `appointments_database_checkout.py` — Tests query performance on a PostgreSQL database storing data about medical appointments.
- `flight_database_checkout.py` — Benchmarks SQL queries on a PostgreSQL database with flight information.
- `trip_database_checkout.py` — Runs performance tests on a PostgreSQL database containing trip data.

## Prerequisites

- **Python 3.7+**
- **PostgreSQL** (configured in `pgAdmin`)
- **psycopg2** (Python library for PostgreSQL connectivity)
- **psutil** (for tracking system resource usage)

Install dependencies by running:

```bash
pip install psycopg2 psutil


#USAGE
python appointments_database_checkout.py
python flight_database_checkout.py
python trip_database_checkout.py

