function sendHttpRequest() {
    // Get all form fields
    const departureCity = document.getElementById('departureCity').value;
    const arrivalCity = document.getElementById('arrivalCity').value;
    const departureTime = document.getElementById('departureTime').value;
    const arrivalTime = document.getElementById('arrivalTime').value;
    const trainType = document.getElementById('trainType').value;
    
    // Get selected days from checkboxes (returns array like ["Mon", "Fri"])
    const selectedDays = Array.from(document.querySelectorAll('input[name="days"]:checked'))
        .map(checkbox => checkbox.value);
    const operationDays = selectedDays.length > 0 ? selectedDays : null;
    
    const firstRate = document.getElementById('firstRate').value;
    const secondRate = document.getElementById('secondRate').value;

    // Create request body with all parameters
    const requestBody = {
        departureCity,
        arrivalCity,
        departureTime,
        arrivalTime,
        operationDays,
        firstRate,
        secondRate,
        trainType
    };

    fetch('http://127.0.0.1:5000/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Search results:', data);
        const container = document.querySelector('.container');
        
        if (data.routes && data.routes.length > 0) {
            let html = '<h2>Search Results</h2>';
            html += `<p>Found ${data.routes.length} connection(s)</p>`;
            
            data.routes.forEach(route => {
                html += `
                    <div style="border: 1px solid #ccc; padding: 10px; margin: 10px 0;">
                        <p><strong>Route ID:</strong> ${route.route_id}</p>
                        <p><strong>From:</strong> ${route.departure_city} at ${route.departure_time}</p>
                        <p><strong>To:</strong> ${route.arrival_city} at ${route.arrival_time}</p>
                        <p><strong>Train Type:</strong> ${route.train_type}</p>
                        <p><strong>Days:</strong> ${route.days_of_operation}</p>
                        <p><strong>First Class:</strong> €${route.first_class_rate}</p>
                        <p><strong>Second Class:</strong> €${route.second_class_rate}</p>
                    </div>
                `;
            });
            container.innerHTML = html;
        } else {
            container.innerHTML = '<h2>No connections found</h2><p>Try adjusting your search criteria.</p>';
        }
    })
    .catch(error => {
        console.error('Search failed:', error);
        document.querySelector('.container').innerHTML = '<h2>Error</h2><p>Failed to connect to backend. Make sure the server is running on port 5000.</p>';
    });
}