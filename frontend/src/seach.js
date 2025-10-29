import './App.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios';

    function App() {
      const [message, setMessage] = useState('');
      const [routes, setRoutes] = useState([]);
      const [cities, setCities] = useState([]);

      const [searchForm, setSearchForm] = useState({
        departureCity: '',
        arrivalCity: '',
        trainType: '',
        departureTime: ''
      });

      useEffect(() => {
        axios.get('/message')
          .then(response => setMessage(response.data.message))
          .catch(error => console.error('Error fetching data:', error));

        axios.get('/cities')
          .then(response => setCities(response.data.cities || []))
          .catch(error => console.error('Error fetching cities:', error));
      }, []);


      const searchRoutes = async () => {
        try {
          const response = await axios.post('/search', {
            departureCity: searchForm.departureCity,
            arrivalCity: searchForm.arrivalCity,
            trainType: searchForm.trainType,
            departureTime: searchForm.departureTime
          });
          setRoutes(response.data.routes || []);
          console.log('Search results:', response.data);
        } catch (error) {
          console.error('Search failed:', error);
        }
      };

      const handleInputChange = (e) => {
        setSearchForm({
          ...searchForm,
          [e.target.name]: e.target.value
        });
      };

      return (
        <div className="App">
          <h1>React Frontend with Flask Backend</h1>
          <p>{message}</p>

          <div style={{margin: '20px', padding: '20px', border: '1px solid #ccc'}}>
            <h3>Search Train Routes</h3>

            <input
              type="text"
              name="departureCity"
              placeholder="Departure City (e.g., Paris)"
              value={searchForm.departureCity}
              onChange={handleInputChange}
              style={{margin: '5px', padding: '5px'}}
            />

            <input
              type="text"
              name="arrivalCity"
              placeholder="Arrival City (e.g., London)"
              value={searchForm.arrivalCity}
              onChange={handleInputChange}
              style={{margin: '5px', padding: '5px'}}
            />

            <input
              type="text"
              name="trainType"
              placeholder="Train Type (optional)"
              value={searchForm.trainType}
              onChange={handleInputChange}
              style={{margin: '5px', padding: '5px'}}
            />

            <br/>
            <button onClick={searchRoutes} style={{margin: '10px', padding: '10px'}}>
              Search Routes
            </button>
          </div>

          <div>
            <h3>Cities Available: {cities.length}</h3>
            <h3>Routes Found: {routes.length}</h3>

            {/* Display search results */}
            {routes.length > 0 && (
              <div style={{marginTop: '20px'}}>
                <h4>Search Results:</h4>
                {routes.map((route, index) => (
                  <div key={index} style={{border: '1px solid #eee', padding: '10px', margin: '5px'}}>
                    <p><strong>From:</strong> {route.departure_city}</p>
                    <p><strong>To:</strong> {route.arrival_city}</p>
                    <p><strong>Train:</strong> {route.train_type}</p>
                    <p><strong>Time:</strong> {route.departure_time} - {route.arrival_time}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      );
    }

export default App;
