import React, { useEffect, useState } from "react";
import axios from "axios";
import "./Dashboard.css";

function Dashboard({ user }) {
  const [profile, setProfile] = useState(null);
  const [projects, setProjects] = useState([]);
  const [proposals, setProposals] = useState([]);
  const [messages, setMessages] = useState([]);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) return;

    setLoading(true);

    // Fetch profile
    axios.get(`http://127.0.0.1:8000/api/profiles/?user=${user.id}`)
      .then(res => setProfile(res.data[0]))
      .catch(() => setProfile(null));

    // Fetch projects (for clients)
    if (user.role === "client") {
      axios.get(`http://127.0.0.1:8000/api/projects/?client=${user.id}`)
        .then(res => setProjects(res.data))
        .catch(() => setProjects([]));
    }

    // Fetch proposals (for freelancers)
    if (user.role === "freelancer") {
      axios.get(`http://127.0.0.1:8000/api/proposals/?freelancer=${user.id}`)
        .then(res => setProposals(res.data))
        .catch(() => setProposals([]));
    }

    // Fetch messages
    axios.get(`http://127.0.0.1:8000/api/messages/?receiver=${user.id}`)
      .then(res => setMessages(res.data))
      .catch(() => setMessages([]));

    // Fetch reviews
    axios.get(`http://127.0.0.1:8000/api/reviews/?reviewee=${user.id}`)
      .then(res => setReviews(res.data))
      .catch(() => setReviews([]));

    setLoading(false);
  }, [user]);

  if (!user) return <div>Please log in.</div>;
  if (loading) return <div>Loading dashboard...</div>;

  return (
    <div className="dashboard-container">
      <h2>Dashboard</h2>
      <section className="dashboard-section">
        <h3>Profile</h3>
        {profile ? (
          <div>
            <strong>Name:</strong> {user.username}<br />
            <strong>Role:</strong> {user.role}<br />
            <strong>Skills:</strong> {profile.skills.map(s => s.name).join(", ")}<br />
            <strong>Experience:</strong> {profile.experience}<br />
            <strong>Hourly Rate:</strong> ${profile.hourly_rate}<br />
            <strong>Portfolio:</strong> <a href={profile.portfolio} target="_blank" rel="noopener noreferrer">{profile.portfolio}</a>
          </div>
        ) : (
          <div>No profile found.</div>
        )}
      </section>

      {user.role === "client" && (
        <section className="dashboard-section">
          <h3>Your Projects</h3>
          <ul>
            {projects.map(proj => (
              <li key={proj.id}>
                <strong>{proj.title}</strong> | Budget: ${proj.budget} | Timeline: {proj.timeline}
              </li>
            ))}
          </ul>
        </section>
      )}

      {user.role === "freelancer" && (
        <section className="dashboard-section">
          <h3>Your Proposals</h3>
          <ul>
            {proposals.map(p => (
              <li key={p.id}>
                Project #{p.project} | Bid: ${p.bid} | Status: {p.status}
              </li>
            ))}
          </ul>
        </section>
      )}

      <section className="dashboard-section">
        <h3>Messages</h3>
        <ul>
          {messages.map(m => (
            <li key={m.id}>
              From: {m.sender} | {m.content} | {new Date(m.timestamp).toLocaleString()}
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h3>Reviews</h3>
        <ul className="dashboard-list">
          {reviews.map(r => (
            <li key={r.id}>
              Rating: {r.rating} | {r.comment} | {new Date(r.created_at).toLocaleDateString()}
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}

export default Dashboard;