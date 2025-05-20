import React, { useEffect, useState } from 'react';
import axios from 'axios'; // axios ile backende istek gönderilir.

// Bu sayfa kullanıcının yüklediği dosyaları görüntülemek için kullanılır.

function FilesPage() { 
  const [files, setFiles] = useState([]);  // files adında bir state değişkeni tanımlar. Başlangıçta boş bir dizi. Bu değişkende kullanıcı dosyalarının listesi tutulacak. setFiles ise files’ı güncellemek için kullanılan fonksiyon.
  const [error, setError] = useState(''); //dosya yükleme hatası için bir state değişkeni.
  const [refresh, setRefresh] = useState(false);  // Burada başlangıçta refresh değişkeni false yapılıyor. Daha sonra set ile değişiyor. Mesela bir dosya silindikten sonra true olur.

  useEffect(() => { 
    const fetchFiles = async () => {
      try {
        const res = await axios.get('http://localhost:8000/api/files', {
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
          }
        });
        setFiles(res.data);
      } catch (err) {
        setError('Dosyalar alınamadı. Lütfen tekrar giriş yapın.');
      }
    };
    fetchFiles();
  }, [refresh]);

  const handleDelete = async (id) => { // Parametre olarak silinecek dosyanın id’sini alır.
    try {
      await axios.delete(`http://localhost:8000/api/files/${id}`, { // dosya silme işlemi için axios ile backende delete isteği atılır.
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('token')
        }
      });
      setRefresh(r => !r);
    } catch (err) {
      setError('Dosya silinemedi.');
    }
  };

  return (
    <div className="files-container">
      <h2>Yüklediğiniz Dosyalar</h2>
      {error && <p className="error">{error}</p>}
      <ul>
        {files.map(file => (
          <li key={file.id}>
            {file.filename} ({file.file_type}) - {new Date(file.upload_date).toLocaleString()}
            <button onClick={() => handleDelete(file.id)}>Sil</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default FilesPage; 