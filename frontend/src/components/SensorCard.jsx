export default function SensorCard({ sensor }) {
  return (
    <div
      style={{
        border: "1px solid #ddd",
        borderRadius: "8px",
        padding: "1rem",
        minWidth: "160px",
        boxShadow: "0 1px 3px rgba(0,0,0,0.08)",
      }}
    >
      <h3 style={{ marginTop: 0 }}>{sensor.name}</h3>
      <p style={{ fontSize: "1.4rem", fontWeight: "bold", margin: 0 }}>
        {sensor.value} {sensor.unit}
      </p>
    </div>
  );
}
