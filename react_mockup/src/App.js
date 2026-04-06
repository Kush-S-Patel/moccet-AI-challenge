import React from "react";
import data from "./optimized_notifications.json";

function formatTime(ts) {
  const d = new Date(ts);
  return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function formatDate(ts) {
  const d = new Date(ts);
  return d.toDateString();
}

function groupByDay(notifs) {
  const groups = {};

  notifs.forEach(n => {
    const day = formatDate(n.timestamp);
    if (!groups[day]) groups[day] = [];
    groups[day].push(n);
  });

  return groups;
}

function NotificationCard({ n }) {
  return (
    <div style={{
      background: "#1c1c1e",
      color: "white",
      padding: "12px",
      borderRadius: "14px",
      marginBottom: "10px",
      boxShadow: "0 2px 6px rgba(0,0,0,0.4)"
    }}>
      <div style={{ fontSize: "12px", opacity: 0.6 }}>
        [{n.source.toUpperCase()}] {formatTime(n.timestamp)}
      </div>

      <div style={{ fontWeight: "600", fontSize: "15px" }}>
        {n.content.title}
      </div>

      <div style={{ fontSize: "14px", opacity: 0.85 }}>
        {n.content.body}
      </div>
    </div>
  );
}

function App() {
  const grouped = groupByDay(data);

  return (
    <div style={{
      background: "#000",
      minHeight: "100vh",
      padding: "20px",
      fontFamily: "system-ui"
    }}>
      <h2 style={{ color: "white" }}>iOS Notification Simulation</h2>

      {Object.entries(grouped).map(([day, notifs]) => (
        <div key={day} style={{ marginBottom: "30px" }}>
          <h3 style={{ color: "#aaa" }}>{day}</h3>

          {notifs.map((n, i) => {
            const hour = new Date(n.timestamp).getHours();

            // Quiet hours visualization
            if (hour >= 22 || hour < 7) {
              return (
                <div key={i} style={{
                  color: "#666",
                  margin: "10px 0",
                  fontStyle: "italic"
                }}>
                  --- Quiet Hours (10PM–7AM) ---
                </div>
              );
            }

            return <NotificationCard key={i} n={n} />;
          })}
        </div>
      ))}
    </div>
  );
}

export default App;