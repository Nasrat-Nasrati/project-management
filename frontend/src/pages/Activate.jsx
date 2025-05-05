// src/Activate.js
import React, { useState } from 'react';
import axios from 'axios';

function Activate() {
  const [code, setCode] = useState('');
  const [message, setMessage] = useState('');

  const handleActivate = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/api/activate/', {
        code
      });
      setMessage('Account activated successfully! You can now login.');
    } catch (error) {
      setMessage('Activation failed. ' + error.response.data.error);
    }
  };

  return (
    <div>
      <h2>Activate Account</h2>
      <form onSubmit={handleActivate}>
        <input placeholder="Activation Code" value={code} onChange={(e) => setCode(e.target.value)} />
        <button type="submit">Activate</button>
      </form>
      <p>{message}</p>
    </div>
  );
}

export default Activate;
