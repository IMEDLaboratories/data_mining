"use client";
import axios from "axios";
import React, { useState } from "react";
import { Bar, Line, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  ArcElement  // Dodaj ArcElement tutaj
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  ArcElement  // Zarejestruj ArcElement tutaj
);

export default function App() {
  interface Result {
    database: string;
    query: string;
    executionTime: number;
    avgRam: number;
    maxRam: number;
    avgCpu: number;
    maxCpu: number;
  }

  const [selectedDatabase, setSelectedDatabase] = useState<string>('python_generator_data');
  const [results, setResults] = useState<Result[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState('');

  // Function to handle database change
  const handleDatabaseChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedDatabase(e.target.value);
    setResults(null); // Reset results on database change
  };

  // Function to run query
  const runQuery = async () => {
    setLoading(true);
    try {
      // Send SQL query to backend
      const response = await axios.post('http://localhost:5000/query', {
        database: selectedDatabase,
        query: query,
      });
      setResults(response.data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  // Example data for charts
  const chartData = {
    labels: Array.isArray(results) ? results.map((_, index) => `Result ${index + 1}`) : [],
    datasets: [
      {
        label: 'Execution Time (ms)',
        data: Array.isArray(results) ? results.map((result) => result.executionTime) : [],
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
      // Dodaj inne zestawy danych, jeśli są potrzebne
   
      {
        label: 'Average RAM (MB)',
        data: results?.map(result => result.avgRam) || [],
        backgroundColor: 'rgba(54, 162, 235, 0.5)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      },
      {
        label: 'Average CPU (%)',
        data: results?.map(result => result.avgCpu) || [],
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center p-8">
      <h1 className="text-3xl font-bold mb-6">Database Performance Metrics</h1>

      {/* Database Selection */}
      <div className="flex items-center mb-4 space-x-4">
        <select
          value={selectedDatabase}
          onChange={handleDatabaseChange}
          className="bg-gray-800 text-white px-4 py-2 rounded-md"
        >
          <option value="python_generator_data">Appointments</option>
          <option value="loty">Flights</option>
          <option value="trip_database">Trips</option>
        </select>
      </div>

      {/* SQL Query Input */}
      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Write your SQL query here"
        rows={5}
        cols={50}
        className="w-full max-w-2xl bg-gray-800 text-white p-4 rounded-md mb-4"
      />

      {/* Run Query Button */}
      <button
        onClick={runQuery}
        disabled={loading}
        className={`px-4 py-2 rounded-md ${loading ? 'bg-gray-600' : 'bg-blue-600 hover:bg-blue-500'} transition duration-300`}
      >
        {loading ? 'Processing...' : 'Run Query'}
      </button>

      {/* Displaying Results */}
      {results && (
        <div className="mt-8 w-full max-w-4xl">
          <h2 className="text-xl font-semibold mb-4">Results for {selectedDatabase}:</h2>

          {/* Render charts based on results */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-gray-800 p-4 rounded-lg">
              <h3 className="text-lg font-medium mb-2">Execution Time</h3>
              <Bar data={{ labels: chartData.labels, datasets: [chartData.datasets[0]] }} options={{ responsive: true }} />
            </div>
            <div className="bg-gray-800 p-4 rounded-lg">
              <h3 className="text-lg font-medium mb-2">Average RAM Usage</h3>
              <Line data={{ labels: chartData.labels, datasets: [chartData.datasets[1]] }} options={{ responsive: true }} />
            </div>
            <div className="bg-gray-800 p-4 rounded-lg">
              <h3 className="text-lg font-medium mb-2">Average CPU Usage</h3>
              <Pie data={{ labels: chartData.labels, datasets: [chartData.datasets[2]] }} options={{ responsive: true }} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
