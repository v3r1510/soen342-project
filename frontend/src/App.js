import './App.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios';

    function App() {
      const [message, setMessage] = useState('');

      useEffect(() => {
        axios.get('/message') // This will be proxied to http://localhost:5000/api/data
          .then(response => setMessage(response.data.message))
          .catch(error => console.error('Error fetching data:', error));
      }, []);

      return (
        <div className="App">
          <h1>React Frontend with Flask Backend</h1>
          <p>{message}</p>
        </div>
      );
    }

export default App;
