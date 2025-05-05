


import React, { useState } from 'react';
import axios from 'axios';

function Signup() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    phone: '',
    address: '',
    profile_picture: null  // برای عکس
  });

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    if (files) {
      setFormData({ ...formData, [name]: files[0] });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleSignup = async (e) => {
    e.preventDefault();

    const signupData = new FormData();
    signupData.append('username', formData.username);
    signupData.append('email', formData.email);
    signupData.append('password', formData.password);
    signupData.append('first_name', formData.first_name);
    signupData.append('last_name', formData.last_name);
    signupData.append('profile.phone', formData.phone);
    signupData.append('profile.address', formData.address);
    signupData.append('profile.profile_picture', formData.profile_picture);

    try {
      const response = await axios.post('http://localhost:8000/api/signup/', signupData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      console.log('Signup success', response.data);
    } catch (error) {
      console.error('Signup failed', error.response?.data || error.message);
    }
  };

  return (
    <form onSubmit={handleSignup}>
      <input name="username" placeholder="Username" onChange={handleChange} />
      <input name="email" placeholder="Email" onChange={handleChange} />
      <input name="password" placeholder="Password" type="password" onChange={handleChange} />
      <input name="first_name" placeholder="First Name" onChange={handleChange} />
      <input name="last_name" placeholder="Last Name" onChange={handleChange} />
      <input name="phone" placeholder="Phone" onChange={handleChange} />
      <input name="address" placeholder="Address" onChange={handleChange} />
      <input name="profile_picture" type="file" accept="image/*" onChange={handleChange} />
      <button type="submit">Signup</button>
    </form>
  );
}

export default Signup;

