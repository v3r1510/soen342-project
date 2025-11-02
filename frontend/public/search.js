function sendHttpRequest() {
    // Get all form fields
    const departureCity = document.getElementById('departureCity').value;
    const arrivalCity = document.getElementById('arrivalCity').value;
    const departureTime = document.getElementById('departureTime').value;
    const arrivalTime = document.getElementById('arrivalTime').value;
    const trainType = document.getElementById('trainType').value;
    
   
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
        document.querySelector('.container').innerHTML = JSON.stringify(data.routes);
    })
    .catch(error => {
        console.error('Search failed:', error);
    });
}