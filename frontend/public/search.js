let currentResults = [];

function sendHttpRequest() {
    const departureCity = document.getElementById('departureCity').value;
    const arrivalCity = document.getElementById('arrivalCity').value;
    const departureTime = document.getElementById('departureTime').value;
    const arrivalTime = document.getElementById('arrivalTime').value;
    const trainType = document.getElementById('trainType').value;
    
    // take checked day checkboxes as an array:
    const selectedDays = Array.from(document.querySelectorAll('input[name="days"]:checked'))
        .map(checkbox => checkbox.value);
    const operationDays = selectedDays.length > 0 ? selectedDays : null;
    
    const firstRate = document.getElementById('firstRate').value;
    const secondRate = document.getElementById('secondRate').value;

    // request body with all parameters:
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
        displayResults(data.routes);
    })
    .catch(error => {
        console.error('Search failed:', error);
    });
}

function displayResults(routes) {
    currentResults = routes;
    const container = document.querySelector('.search-results');
    container.innerHTML = '';
    
    const sortingDiv = document.createElement('div');
    sortingDiv.className = 'sorting-buttons';
    sortingDiv.innerHTML = `
        <h3>Sort by:</h3>
        <button onclick="sortResults('duration')">Trip Duration</button>
        <button onclick="sortResults('price-first')">First Class Price</button>
        <button onclick="sortResults('price-second')">Second Class Price</button>
    `;
    container.appendChild(sortingDiv);
    
    const resultsDiv = document.createElement('div');
    resultsDiv.id = 'results-container';
    displaySortedResults(routes, resultsDiv);
    container.appendChild(resultsDiv);
}

function sortResults(parameter) {
    const sortedResults = [...currentResults];
    
    // sorting by comparison:
    switch(parameter) {
        case 'duration':
            sortedResults.sort((a, b) => parseInt(a.trip_time) - parseInt(b.trip_time));
            break;
        case 'price-first':
            sortedResults.sort((a, b) => parseFloat(a.first_class_rate) - parseFloat(b.first_class_rate));
            break;
        case 'price-second':
            sortedResults.sort((a, b) => parseFloat(a.second_class_rate) - parseFloat(b.second_class_rate));
            break;
    }
    
    const resultsContainer = document.getElementById('results-container');
    displaySortedResults(sortedResults, resultsContainer);
}

function displaySortedResults(routes, container) {
    container.innerHTML = '';
    
    if (routes.length === 0) {
        container.innerHTML = '<p>No results found</p>';
        return;
    }

    // creating display card for each connection:
    routes.forEach(route => {
        const routeDiv = document.createElement('div');
        routeDiv.className = 'route-item';
        routeDiv.innerHTML = `
            <h3>${route.departure_city} → ${route.arrival_city}</h3>
            <p>Departure: <strong>${route.departure_time}</strong> | Arrival: <strong>${route.arrival_time}</strong></p>
            <p>Duration: <strong>${route.trip_time} minutes</strong></p>
            <p>Train Type: <strong>${route.train_type}</strong></p>
            <p>Operating Days: <strong>${route.days_of_operation}</strong></p>
            <p>First Class: <strong>€${route.first_class_rate}</strong> | Second Class: <strong>€${route.second_class_rate}</strong></p>
            <button onclick="bookNow('${route.id}')" class="book-now" id="book-now">Book Now</button>
        `.trim();
        container.appendChild(routeDiv);

        // event listener for booking button (and store in local storage):
        const bookBtn = routeDiv.querySelector('.book-now');
        bookBtn.addEventListener('click', () => {
            localStorage.setItem('selectedTrip', JSON.stringify(route));
            window.location.href = 'booking.html';
        });
    });
}