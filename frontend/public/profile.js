document.addEventListener('DOMContentLoaded', () => {
    const clientSearchForm = document.getElementById('client-search-form');
    const currentTripsContainer = document.getElementById('current-trips');
    const pastTripsContainer = document.getElementById('past-trips');

    // Fetch trips from backend
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
            // Assuming your backend provides a trip_date field
            const tripDate = trip.trip_date || trip.departure_time;
            if (tripDate < today) {
                pastTrips.push(trip);
            } else {
                currentAndFutureTrips.push(trip);
            }
        });

        return {
            current: currentAndFutureTrips,
            past: pastTrips
        };
    }

    // displaying trip
    function createTripHTML(booking) {
        return `
            <div class="trip-card">
                <h4>${trip.departure_city} → ${trip.arrival_city}</h4>
                <p>Trip ID: ${trip.trip_id}</p>
                <p>Departure: ${trip.departure_time}</p>
                <p>Arrival: ${trip.arrival_time}</p>
                <p>Travelers: ${trip.travelers ? trip.travelers.length : 0}</p>
            </div>
        `;
    }
    //might need later so are keeping the orginial one
    // displaying trip
 //    function createTripHTML(booking) {
 //        return `
 //            <div class="trip-card">
 //                <h4>${booking.trip.departure_city} → ${booking.trip.arrival_city}</h4>
 //                <p>Trip Date: ${booking.trip.trip_date}</p>
 //                <p>Departure: ${booking.trip.departure_time}</p>
 //                <p>Arrival: ${booking.trip.arrival_time}</p>
 //                <p>Duration: ${booking.trip.trip_time} hours</p>
 //                <p>Booking ID: ${booking.bookingId}</p>
 //                <p>Travelers: ${booking.travellers.map(t =>
 //                    `${t.firstName} ${t.lastName} (${t.class} class)`).join(', ')}</p>
 //            </div>
 //        `;
 //    }
    // make trips show in their corresponding containers:
    function displayTrips(sortedTrips) {
        currentTripsContainer.innerHTML = sortedTrips.current.length > 0
            ? sortedTrips.current.map(createTripHTML).join('')
            : '<p>No current or upcoming trips found.</p>';

        pastTripsContainer.innerHTML = sortedTrips.past.length > 0
            ? sortedTrips.past.map(createTripHTML).join('')
            : '<p>No past trips found.</p>';
    }

    // hndle form submission:
    clientSearchForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const clientId = document.getElementById('client-id').value;
        const trips = await getClientTrips(clientId);
        const sortedTrips = sortTrips(trips);

        displayTrips(sortedTrips);
    });
});