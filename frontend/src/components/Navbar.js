
 

import React from 'react'; 
import { Link, useNavigate } from 'react-router-dom'; 

function Navbar() {  
  const navigate = useNavigate(); 
  const isLoggedIn = !!localStorage.getItem('token'); // Kullanıcı giriş yapmış mı yapmamış mı kontrol ediliyor. localStorage ile token kontrolü sağlanıyor.
  // !! ile boolean değer döndürülüyor.

  const handleLogout = () => { // Çıkış yapma işlemi.
    localStorage.removeItem('token'); // localStorage'dan token siliniyor.
    navigate('/login'); // login sayfasına yönlendiriliyor.
  };

  return ( 
    <nav className="navbar">
      <Link to="/files">Dosyalarım</Link>
      <Link to="/upload">Dosya Yükle</Link>
      {isLoggedIn ? ( // kullanıcı giriş yapmışsa (isLoggedIn true).
        <button onClick={handleLogout}>Çıkış</button> // Sadece çıkış yapma butonu görünür.
      ) : (
        <>     
          <Link to="/login">Giriş</Link>
          <Link to="/register">Kayıt</Link>
        </>
      )}
    </nav>
  );
}

export default Navbar;  // Bu sayede navbar bileşeni dışarıdan import edilebilir.