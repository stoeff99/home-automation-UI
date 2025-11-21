// frontend/src/App.jsx

import { useEffect, useState } from "react";
import Dashboard from "./components/Dashboard";

function App() {
  const [sensors, setSensors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/api/sensors/current")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch");
        return res.json();
      })
      .then((data) => {
        setSensors(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching sensors:", err);
        setError("Failed to load sensors");
        setLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto flex min-h-screen max-w-6xl flex-col px-4 py-6 lg:px-8">
        <header className="mb-6 flex items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">
              Home Automation
            </h1>
            <p className="mt-1 text-sm text-slate-400">
              Live data from MQTT, InfluxDB &amp; Loxone
            </p>
          </div>
          <div className="hidden items-center gap-2 rounded-full border border-slate-800 bg-slate-900/70 px-3 py-1 text-xs text-slate-400 shadow-sm shadow-slate-900/50 sm:flex">
            <span className="mr-1 h-2 w-2 rounded-full bg-emerald-500" />
            Backend connected
          </div>
        </header>

        {loading && (
          <div className="flex flex-1 items-center justify-center">
            <div className="h-10 w-10 animate-spin rounded-full border-2 border-slate-600 border-t-brand-500" />
          </div>
        )}

        {!loading && error && (
          <div className="card mx-auto mt-10 max-w-md p-4 text-center">
            <p className="text-sm text-red-400">{error}</p>
          </div>
        )}

        {!loading && !error && (
          <main className="flex-1">
            <Dashboard sensors={sensors} />
          </main>
        )}

        <footer className="mt-6 border-t border-slate-900 pt-3 text-xs text-slate-500">
          <span>Powered by React + Vite + Flask + MQTT</span>
        </footer>
      </div>
    </div>
  );
}

export default App;

