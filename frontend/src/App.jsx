// App.jsx
import Dashboard from "./pages/Dashboard";

function App() {
  // Example user object for testing
  const user = {
    id: 1,
    username: "freelancer1",
    role: "freelancer", // or "client"
  };

  return <Dashboard user={user} />;
}

export default App;