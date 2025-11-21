// frontend/src/components/SensorCard.jsx

export default function SensorCard({ sensor, active, onClick }) {
  const { name, value, unit, id, group } = sensor;

  const isCritical =
    typeof value === "number" &&
    (Number.isNaN(value) || !Number.isFinite(value));

  return (
    <button
      type="button"
      onClick={onClick}
      className={`card relative flex flex-col gap-2 p-4 text-left transition ${
        active
          ? "border-brand-500/80 ring-1 ring-brand-500/50"
          : "hover:translate-y-0.5 hover:border-brand-500/70 hover:shadow-brand-500/20"
      }`}
    >
      <div className="flex items-center justify-between gap-2">
        <h3 className="truncate text-sm font-medium text-slate-50">
          {name || id}
        </h3>
        <span className="text-[10px] uppercase tracking-wide text-slate-500">
          {group || "Sensor"}
        </span>
      </div>

      <div className="flex items-baseline gap-1">
        {value === undefined || value === null ? (
          <span className="text-sm text-slate-500">No data</span>
        ) : (
          <>
            <span className="text-2xl font-semibold tabular-nums text-slate-50">
              {typeof value === "number" ? value.toFixed(2) : value}
            </span>
            {unit && (
              <span className="text-xs text-slate-400">
                {unit}
              </span>
            )}
          </>
        )}
      </div>

      <div className="mt-1 flex items-center justify-between text-[11px] text-slate-500">
        <span className="truncate">ID: {id}</span>
        <span
          className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 ${
            isCritical
              ? "bg-red-500/10 text-red-400"
              : "bg-emerald-500/10 text-emerald-400"
          }`}
        >
          <span className="h-1.5 w-1.5 rounded-full bg-current" />
          live
        </span>
      </div>
    </button>
  );
}
