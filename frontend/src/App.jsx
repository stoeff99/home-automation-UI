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

  if (loading) return <div style={{ padding: "1rem" }}>Loading...</div>;
  if (error) return <div style={{ padding: "1rem", color: "red" }}>{error}</div>;

  return <Dashboard sensors={sensors} />;
}

export default App;
