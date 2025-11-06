// to retrieve the selected trip data:
const selectedTrip = JSON.parse(localStorage.getItem('selectedTrip'));

if (!selectedTrip) {
    alert('No trip selected. Redirecting to search...');
    window.location.href = 'search.html';
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('trip-summary').innerHTML = `
        <h2>Selected Connection: </h2>
        <p><strong>Route:</strong> ${selectedTrip.departure_city} → ${selectedTrip.arrival_city}</p>
        <p><strong>Departure:</strong> ${selectedTrip.departure_time}</p>
        <p><strong>Arrival:</strong> ${selectedTrip.arrival_time}</p>
        <p><strong>Duration:</strong> ${selectedTrip.trip_time} minutes</p>
        <p><strong>First Class:</strong> €${selectedTrip.first_class_rate}</p>
        <p><strong>Second Class:</strong> €${selectedTrip.second_class_rate}</p>
    `;
});