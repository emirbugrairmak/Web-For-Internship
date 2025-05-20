import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function RegisterPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const res = await axios.post('http://localhost:8000/api/register', {
        username,
        email,
        password
      });
      localStorage.setItem('token', res.data.access_token);
      navigate('/files');
    } catch (err) {
      setError('Kayıt başarısız! Kullanıcı adı veya e-posta adresi zaten kayıtlı. Lütfen başka bir kullanıcı adını veya e-posta adresini deneyin.');
    }
  };

  return (
    <div className="register-container">
      <h2>Kayıt Ol</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Kullanıcı Adı" value={username} onChange={e => setUsername(e.target.value)} required />
        <input type="email" placeholder="E-posta" value={email} onChange={e => setEmail(e.target.value)} required />
        <input type="password" placeholder="Şifre" value={password} onChange={e => setPassword(e.target.value)} required />
        <button type="submit">Kayıt Ol</button>
      </form>
      {error && <p className="error">{error}</p>}
      <p>Zaten hesabın var mı? <a href="/login">Giriş Yap</a></p>
    </div>
  );
}

export default RegisterPage; 