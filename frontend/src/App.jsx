import React, { useEffect, useState } from "react";
import axios from "axios";

function Dashboard({ user }) {
  const [projects, setProjects] = useState([]);
  const [proposals, setProposals] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    if (user.role === "freelancer") {
      axios.get("http://127.0.0.1:8000/api/proposals/?freelancer=" + user.id)
        .then(res => setProposals(res.data))
        .finally(() => setLoading(false));
    } else if (user.role === "client") {
      axios.get("http://127.0.0.1:8000/api/projects/?client=" + user.id)
        .then(res => setProjects(res.data))
        .finally(() => setLoading(false));
    }
  }, [user]);

  if (loading) return <div>Loading dashboard...</div>;

  return (
    <div style={{ maxWidth: 800, margin: "40px auto", padding: 24 }}>
      <h2>Dashboard</h2>
      {user.role === "freelancer" && (
        <>
          <h3>Your Proposals</h3>
          <ul>
            {proposals.map(p => (
              <li key={p.id}>
                Project #{p.project} | Bid: ${p.bid} | Status: {p.status}
              </li>
            ))}
          </ul>
        </>
      )}
      {user.role === "client" && (
        <>
          <h3>Your Projects</h3>
          <ul>
            {projects.map(proj => (
              <li key={proj.id}>
                {proj.title} | Budget: ${proj.budget} | Timeline: {proj.timeline}
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

export default Dashboard;