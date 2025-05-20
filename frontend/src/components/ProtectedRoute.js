
// Burada kullanıcılar giriş yapmışsa yani tokena sahipseler belirli sayfalara erişmelerini sağlarız.

import React from 'react';
import { Navigate } from 'react-router-dom'; // Yönlendirme işlemi için Navigate bileşeni import edilir.

function ProtectedRoute({ children }) {
  const token = localStorage.getItem('token');
  if (!token) { // kullanıcı giriş yapmamışsa yani token yoksa login sayfasına yönlendirilir.
    return <Navigate to="/login" />;
  }
  return children; // kullanıcı giriş yapmışsa yani token varsa belirtilen sayfaya yönlendirilir.
}

export default ProtectedRoute; 