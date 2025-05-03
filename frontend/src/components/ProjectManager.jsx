import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ProjectManager = () => {
  const [projects, setProjects] = useState([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [createdBy, setCreatedBy] = useState(1); // ID یوزر، فعلاً ثابت 1

  // گرفتن لیست پروژه‌ها
  const fetchProjects = () => {
    axios.get('http://localhost:8000/api/projects/')
      .then(response => {
        setProjects(response.data);
      })
      .catch(error => {
        console.error('Error fetching projects:', error);
      });
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  // هندل کردن ثبت پروژه جدید
  const handleSubmit = (e) => {
    e.preventDefault();

    axios.post('http://localhost:8000/api/projects/', {
      title: title,
      description: description,
      created_by: createdBy
    })
    .then(response => {
      console.log('پروژه ساخته شد:', response.data);
      // فرم را خالی کن
      setTitle('');
      setDescription('');
      // لیست را دوباره بگیر
      fetchProjects();
    })
    .catch(error => {
      console.error('Error creating project:', error);
    });
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>📋 لیست پروژه‌ها</h2>
      <ul>
        {projects.map(project => (
          <li key={project.id}>
            <strong>{project.title}</strong>: {project.description}
          </li>
        ))}
      </ul>

      <h2>➕ ساخت پروژه جدید</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>عنوان پروژه: </label>
          <input 
            type="text" 
            value={title} 
            onChange={(e) => setTitle(e.target.value)} 
            required 
          />
        </div>
        <div>
          <label>توضیحات: </label>
          <textarea 
            value={description} 
            onChange={(e) => setDescription(e.target.value)} 
            required 
          />
        </div>
        <button type="submit">ثبت پروژه</button>
      </form>
    </div>
  );
};

export default ProjectManager;
