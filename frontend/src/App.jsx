
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Signup from './pages/Signup';
import Activate from "./pages/Activate";
import Login from './pages/Login';
import ProjectManager from './components/ProjectManager';

function App() {
  return (
    <Router>
      <nav>
        <Link to="/signup">Signup</Link> | <Link to="/activate">Activate</Link> | <Link to="/login">Login</Link>
      </nav>
      <Routes>
      <Route path="/project" element={<ProjectManager />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/activate" element={<Activate />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </Router>
  );
}

export default App;



// Protected API call example
const fetchProtectedData = async () => {
  const token = localStorage.getItem('access_token');
  try {
    const response = await axios.get('http://localhost:8000/api/protected/', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    console.log(response.data);
  } catch (error) {
    console.error('Failed to fetch protected data', error);
  }
};


