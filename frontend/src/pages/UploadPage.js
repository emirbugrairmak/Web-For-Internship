import React, { useState } from 'react';
import axios from 'axios';

function UploadPage() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage('');
    setError('');
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Lütfen bir dosya seçin.');
      return;
    }
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await axios.post('http://localhost:8000/api/upload', formData, {
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('token'),
          'Content-Type': 'multipart/form-data'
        }
      });
      setMessage('Dosya başarıyla yüklendi!');
      setFile(null);
    } catch (err) {
      setError('Yükleme başarısız! Sadece PDF, PNG veya JPG dosyaları yüklenebilir.');
    }
  };

  return (
    <div className="upload-container">
      <h2>Dosya Yükle</h2>
      <form onSubmit={handleUpload}>
        <input type="file" accept=".pdf,.png,.jpg" onChange={handleFileChange} />
        <button type="submit">Yükle</button>
      </form>
      {message && <p className="success">{message}</p>}
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default UploadPage; 