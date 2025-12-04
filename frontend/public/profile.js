document.addEventListener('DOMContentLoaded', () => {
    const clientSearchForm = document.getElementById('client-search-form');
    const currentTripsContainer = document.getElementById('current-trips');
    const pastTripsContainer = document.getElementById('past-trips');

    // fetch trips from backend controller
    async function getClientTrips(clientId) {
        try {
            const response = await fetch(`http://127.0.0.1:5000/client/${clientId}/trips`);
            const data = await response.json();
            if (data.success) {
                return data.trips;
            } else {
                console.error('Error fetching trips:', data.error);
                return [];
            }
        } catch (error) {
            console.error('Failed to fetch trips:', error);
            return [];
        }
    }

    // Sort trips by date
    function sortTrips(trips) {
        const today = new Date().toISOString().split('T')[0];
        const currentAndFutureTrips = [];
        const pastTrips = [];

        trips.forEach(trip => {
            if (trip.date < today) {
                pastTrips.push(trip);
            } else {
                currentAndFutureTrips.push(trip);
            }
        });

        // Sort current trips by date (earliest first)
        currentAndFutureTrips.sort((a, b) => a.date.localeCompare(b.date));

        // Sort past trips by date (most recent first)
        pastTrips.sort((a, b) => b.date.localeCompare(a.date));

        return {
            current: currentAndFutureTrips,
            past: pastTrips
        };
    }

    // displaying trip based on actual backend structure
    function createTripHTML(trip) {
        // Determine the price based on travel class
        const travelClass = trip.travel_class || 'second'; // Default to second if not specified
        const price = travelClass === 'first'
            ? trip.connection.first_class_rate
            : trip.connection.second_class_rate;

        // Capitalize first letter for display
        const travelClassDisplay = travelClass.charAt(0).toUpperCase() + travelClass.slice(1);

        return `
            <div class="trip-card">
                <h4>${trip.connection.departure_city} → ${trip.connection.arrival_city}</h4>
                <p><strong>Date:</strong> ${trip.date}</p>
                <p><strong>Ticket ID:</strong> ${trip.ticket.ticket_id}</p>
                <p><strong>Departure:</strong> ${trip.connection.departure_time}</p>
                <p><strong>Arrival:</strong> ${trip.connection.arrival_time}</p>
                <p><strong>Duration:</strong> ${trip.connection.trip_time}</p>
                <p><strong>Train Type:</strong> ${trip.connection.train_type}</p>
                <p><strong>Days of Operation:</strong> ${trip.connection.days_of_operation}</p>
                <p><strong>Traveler:</strong> ${trip.client.name} (Age: ${trip.client.age})</p>
                <p><strong>Travel Class:</strong> ${travelClassDisplay} Class</p>
                <p><strong>Price:</strong> €${price}</p>
            </div>
        `;
    }

    // make trips show in their corresponding containers:
    function displayTrips(sortedTrips) {
        currentTripsContainer.innerHTML = sortedTrips.current.length > 0
            ? sortedTrips.current.map(createTripHTML).join('')
            : '<p>No current or upcoming trips found.</p>';

        pastTripsContainer.innerHTML = sortedTrips.past.length > 0
            ? sortedTrips.past.map(createTripHTML).join('')
            : '<p>No past trips found.</p>';
    }

    // handle form submission:
    clientSearchForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const clientId = document.getElementById('client-id').value;
        const trips = await getClientTrips(clientId);
        const sortedTrips = sortTrips(trips);

        displayTrips(sortedTrips);
    });
});