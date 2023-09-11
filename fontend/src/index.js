import React from 'react';
import ReactDOM from 'react-dom';
import App from './App'; // Import component chính của ứng dụng
import reportWebVitals from './reportWebVitals'; // Import reportWebVitals

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root'),
);

// Gửi các thông số hiệu suất đến reportWebVitals
reportWebVitals();
