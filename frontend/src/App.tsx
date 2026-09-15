import { useEffect, useState } from "react";
import api from "./services/api";

function App() {
  const [status, setStatus] = useState("Checking backend...");

  useEffect(() => {
    api
      .get("/health")
      .then((response) => {
        if (response.data.status === "healthy") {
          setStatus("Backend Connected ✓");
        }
      })
      .catch(() => {
        setStatus("Backend Not Connected ✗");
      });
  }, []);

  return (
    <div>
      <h1>Devora</h1>
      <p>{status}</p>
    </div>
  );
}

export default App;