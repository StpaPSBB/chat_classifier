import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Проверка формата
    if (!file.name.endsWith('.json')) {
      setError('Пожалуйста, загрузите файл в формате JSON');
      return;
    }

    setIsLoading(true);
    setError(null);
    setSuccess(false);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(
        'http://localhost:8000/classifier/classify',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          responseType: 'blob',
        }
      );

      // Создаем ссылку для скачивания
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      
      // Получаем имя файла из headers
      const contentDisposition = response.headers['content-disposition'];
      let filename = 'classification.png';
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="(.+)"/);
        if (filenameMatch && filenameMatch[1]) {
          filename = filenameMatch[1];
        }
      }
      
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      setSuccess(true);
      
      // Показываем статистику если есть в headers
      const distribution = response.headers['x-distribution'];
      if (distribution) {
        const stats = JSON.parse(distribution);
        console.log('Статистика классификации:', stats);
        // Можно показать alert с краткой статистикой
        const total = Object.values(stats).reduce((a, b) => a + b, 0);
        alert(`Файл успешно обработан!\n\nСообщений проанализировано: ${total}\n\nДиаграмма сохранена как: ${filename}`);
      }

    } catch (err) {
      console.error('Ошибка:', err);
      setError(
        err.response?.data?.detail || 
        'Произошла ошибка при обработке файла'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      const file = files[0];
      if (file.name.endsWith('.json')) {
        // Создаем искусственное событие для input
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        document.getElementById('file-input').files = dataTransfer.files;
        
        // Триггерим изменение
        const event = new Event('change', { bubbles: true });
        document.getElementById('file-input').dispatchEvent(event);
      } else {
        setError('Пожалуйста, загрузите файл в формате JSON');
      }
    }
  };

  return (
    <div className="App">
      <header className="header">
        <h1>Классификатор сообщений в чатах</h1>
        <p>Загрузите JSON файл для анализа</p>
      </header>

      <main className="main">
        <div 
          className={`upload-area ${isLoading ? 'loading' : ''}`}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
        >
          <input
            id="file-input"
            type="file"
            accept=".json"
            onChange={handleFileUpload}
            disabled={isLoading}
            style={{ display: 'none' }}
          />
          
          {isLoading ? (
            <div className="loading-state">
              <div className="spinner"></div>
              <p>Обработка файла...</p>
            </div>
          ) : (
            <label htmlFor="file-input" className="upload-label">
              <div className="upload-icon">📁</div>
              <div className="upload-text">
                <strong>Нажмите для выбора файла</strong>
                <span>или перетащите JSON файл сюда</span>
              </div>
              <div className="file-format">Только .json файлы</div>
            </label>
          )}
        </div>

        {error && (
          <div className="error">
            <p>{error}</p>
            <button 
              onClick={() => {
                setError(null);
                setSuccess(false);
              }}
              className="reset-btn"
            >
              Попробовать снова
            </button>
          </div>
        )}

        {success && (
          <div className="success">
            <p>Файл успешно обработан и скачан!</p>
            <button 
              onClick={() => {
                setSuccess(false);
                document.getElementById('file-input').value = '';
              }}
              className="reset-btn"
            >
              Загрузить другой файл
            </button>
          </div>
        )}

        <div className="instructions">
          <h3>Инструкция:</h3>
          <ol>
            <li>Загрузите JSON файл с историей чата</li>
            <li>Система проанализирует сообщения</li>
            <li>Автоматически скачается PNG файл с диаграммой</li>
          </ol>
        </div>
      </main>

      <footer className="footer">
        <p>Система классификации сообщений по 6 категориям</p>
      </footer>
    </div>
  );
}

export default App;