// frontend/src/components/Dashboard.jsx

import { useState, useMemo, useEffect } from "react";
import SensorCard from "./SensorCard";
import SensorChart from "./SensorChart";

export default function Dashboard({ sensors }) {
  const [search, setSearch] = useState("");
  const [selectedSensor, setSelectedSensor] = useState(null);

  const filteredSensors = useMemo(() => {
    const term = search.trim().toLowerCase();
    if (!term) return sensors;

    return sensors.filter((s) => {
      const name = (s.name || "").toLowerCase();
      const id = (s.id || "").toLowerCase();
      const group = (s.group || "").toLowerCase();
      return (
        name.includes(term) ||
        id.includes(term) ||
        group.includes(term)
      );
    });
  }, [sensors, search]);

  const grouped = useMemo(() => {
    return filteredSensors.reduce((acc, s) => {
      const key = s.group || "Other";
      if (!acc[key]) acc[key] = [];
      acc[key].push(s);
      return acc;
    }, {});
  }, [filteredSensors]);

  const groupEntries = Object.entries(grouped).sort((a, b) =>
    a[0].localeCompare(b[0])
  );

  // If the previously selected sensor disappears (e.g. config change),
  // clear the selection instead of auto-selecting another one.
  useEffect(() => {
    if (
      selectedSensor &&
      !sensors.find((s) => s.id === selectedSensor.id)
    ) {
      setSelectedSensor(null);
    }
  }, [sensors, selectedSensor]);

  // Helper: toggle selection when clicking a tile
  const handleSelect = (sensor) => {
    if (selectedSensor && selectedSensor.id === sensor.id) {
      // click again on the same tile -> hide chart
      setSelectedSensor(null);
    } else {
      setSelectedSensor(sensor);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header row: count + search */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="text-sm text-slate-400">
          <span className="font-medium text-slate-200">
            {filteredSensors.length}
          </span>{" "}
          sensors visible
        </div>

        <div className="relative w-full max-w-xs">
          <input
            type="text"
            placeholder="Filter by name, group, id..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full rounded-full border border-slate-800 bg-slate-900/80 px-4 py-2 pr-9 text-sm text-slate-100 placeholder:text-slate-500 shadow-sm shadow-slate-900/50 focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
          />
          <span className="pointer-events-none absolute inset-y-0 right-3 flex items-center text-slate-500">
            ⌕
          </span>
        </div>
      </div>

      {/* Sensor groups */}
      {groupEntries.length === 0 && (
        <div className="card p-6 text-center text-sm text-slate-400">
          No sensors match your filter.
        </div>
      )}

      {groupEntries.map(([groupName, groupSensors]) => (
        <section key={groupName} className="space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-400">
              {groupName}
            </h2>
            <span className="text-xs text-slate-500">
              {groupSensors.length} sensor
              {groupSensors.length !== 1 && "s"}
            </span>
          </div>

          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {groupSensors.map((s) => (
              <SensorCard
                key={s.id}
                sensor={s}
                active={selectedSensor && selectedSensor.id === s.id}
                onClick={() => handleSelect(s)}
              />
            ))}
          </div>
        </section>
      ))}

      {/* Chart ONLY when a sensor is selected */}
      {selectedSensor && (
        <SensorChart sensor={selectedSensor} />
      )}
    </div>
  );
}
