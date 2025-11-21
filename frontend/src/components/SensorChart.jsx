// frontend/src/components/SensorChart.jsx

import { useEffect, useState, useCallback } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

const RANGE_OPTIONS = [
  { label: "1h", value: "1h" },
  { label: "6h", value: "6h" },
  { label: "24h", value: "24h" },
  { label: "7d", value: "7d" },
];

export default function SensorChart({ sensor }) {
  const [range, setRange] = useState("6h");
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const { id, name, unit } = sensor;

  const fetchHistory = useCallback(() => {
    fetch(`/api/sensors/${id}/history?range=${range}`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch history");
        return res.json();
      })
      .then((points) => {
        const mapped = points.map((p) => ({
          time: new Date(p.time),
          value: p.value,
        }));
        setData(mapped);
        setLoading(false);
        setError("");
      })
      .catch((err) => {
        console.error("Error fetching history:", err);
        setError("Failed to load history");
        setLoading(false);
      });
  }, [id, range]);

  // Initial + range change load
  useEffect(() => {
    setLoading(true);
    fetchHistory();
  }, [fetchHistory]);

  // Poll every 10 seconds for near real-time updates
  useEffect(() => {
    const interval = setInterval(fetchHistory, 10000);
    return () => clearInterval(interval);
  }, [fetchHistory]);

  const formattedData = data.map((d) => ({
    ...d,
    label: d.time.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
  }));

  return (
    <div className="card mt-4 p-4">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
        <div>
          <h2 className="text-sm font-semibold text-slate-100">
            {name || id}
          </h2>
          <p className="text-xs text-slate-500">
            Historical data ({range})
          </p>
        </div>

        <div className="flex gap-1 rounded-full bg-slate-900/70 p-1 text-xs">
          {RANGE_OPTIONS.map((opt) => (
            <button
              key={opt.value}
              onClick={() => setRange(opt.value)}
              className={`rounded-full px-2 py-0.5 ${
                range === opt.value
                  ? "bg-brand-500 text-white"
                  : "text-slate-400 hover:bg-slate-800"
              }`}
            >
              {opt.label}
            </button>
          ))}
        </div>
      </div>

      {loading && (
        <div className="flex h-40 items-center justify-center text-xs text-slate-400">
          Loading history…
        </div>
      )}

      {!loading && error && (
        <div className="h-40 text-xs text-red-400">{error}</div>
      )}

      {!loading && !error && formattedData.length === 0 && (
        <div className="flex h-40 items-center justify-center text-xs text-slate-400">
          No data points in selected range.
        </div>
      )}

      {!loading && !error && formattedData.length > 0 && (
        <div className="h-56 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={formattedData} margin={{ top: 10, right: 16, bottom: 0, left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
              <XAxis
                dataKey="label"
                tick={{ fontSize: 10, fill: "#9ca3af" }}
                tickLine={false}
                axisLine={false}
              />
              <YAxis
                tick={{ fontSize: 10, fill: "#9ca3af" }}
                tickLine={false}
                axisLine={false}
                width={40}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#020617",
                  borderRadius: "0.5rem",
                  border: "1px solid #1f2937",
                  fontSize: "0.75rem",
                }}
                labelFormatter={(label, payload) => {
                  if (!payload?.[0]) return "";
                  const d = payload[0].payload.time;
                  return d.toLocaleString();
                }}
                formatter={(value) => [`${value} ${unit || ""}`, name || id]}
              />
              <Line
                type="monotone"
                dataKey="value"
                dot={false}
                stroke="#3b82f6"
                strokeWidth={2}
                isAnimationActive={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
