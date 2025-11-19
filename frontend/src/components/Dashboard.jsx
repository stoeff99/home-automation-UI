import SensorCard from "./SensorCard";

export default function Dashboard({ sensors }) {
  return (
    <div style={{ padding: "1.5rem", fontFamily: "sans-serif" }}>
      <h1 style={{ marginBottom: "1rem" }}>Home Automation Dashboard</h1>
      <div
        style={{
          display: "flex",
          gap: "1rem",
          flexWrap: "wrap",
        }}
      >
        {sensors.map((s) => (
          <SensorCard key={s.id} sensor={s} />
        ))}
      </div>
    </div>
  );
}
