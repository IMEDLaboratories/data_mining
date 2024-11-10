"use client";
import axios from "axios";
import React, { useState } from "react";

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

  const [results, setResults] = useState<Result[] | null>(null);
  const [loading, setLoading] = useState(false);

  const runScripts = async () => {
    setLoading(true);
    try {
      await axios.post("http://localhost:5000/run"); // Endpoint to run scripts
      const response = await axios.get<Result[]>("http://localhost:5000/results"); // Fetch results
      setResults(response.data);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Database Performance Metrics</h1>
      <button onClick={runScripts} disabled={loading}>
        {loading ? "Processing..." : "Run Scripts and Fetch Results"}
      </button>
      {results && (
        <div>
          <h2>Results:</h2>
          <pre>{JSON.stringify(results, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
