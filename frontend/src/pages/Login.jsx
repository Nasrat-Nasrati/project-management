// // src/Login.js
// import React, { useState } from 'react';
// import axios from 'axios';

// function Login() {
//   const [username, setUsername] = useState('');
//   const [password, setPassword] = useState('');
//   const [message, setMessage] = useState('');

//   const handleLogin = async (e) => {
//     e.preventDefault();
//     try {
//       const response = await axios.post('http://localhost:8000/api/login/', {
//         username,
//         password
//       });
//       const { access, refresh } = response.data;

//       // Save tokens in localStorage
//       localStorage.setItem('access_token', access);
//       localStorage.setItem('refresh_token', refresh);

//       setMessage('Login successful!');
//     } catch (error) {
//       console.error('Error during login:', error);
//       setMessage('Login failed. ' + (error.response ? error.response.data.detail : error.message));
//     }
//   };

//   return (
//     <div>
//       <h2>Login</h2>
//       <form onSubmit={handleLogin}>
//         <input
//           placeholder="Username"
//           value={username}
//           onChange={(e) => setUsername(e.target.value)}
//         />
//         <input
//           placeholder="Password"
//           type="password"
//           value={password}
//           onChange={(e) => setPassword(e.target.value)}
//         />
//         <button type="submit">Login</button>
//       </form>
//       <p>{message}</p>
//     </div>
//   );
// }

// export default Login;


// src/Login.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // 👈 اضافه کن
import axios from 'axios';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate(); // 👈 این hook را تعریف کن

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/login/', {
        username,
        password
      });
      const { access, refresh } = response.data;

      // Save tokens in localStorage
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);

      setMessage('Login successful!');

      // ✅ ریدایرکت به صفحه project بعد از login موفق
      navigate('/project');
      
    } catch (error) {
      console.error('Error during login:', error);
      setMessage('Login failed. ' + (error.response ? error.response.data.detail : error.message));
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Login</button>
      </form>
      <p>{message}</p>
    </div>
  );
}

export default Login;
