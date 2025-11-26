document.addEventListener('DOMContentLoaded', () => {
    const clientSearchForm = document.getElementById('client-search-form');
    const currentTripsContainer = document.getElementById('current-trips');
    const pastTripsContainer = document.getElementById('past-trips');

    // loading bookings from local Storage:
    function getAllBookings() {
        const bookings = [];
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key.startsWith('booking_')) {
                try {
                    const booking = JSON.parse(localStorage.getItem(key));
                    bookings.push(booking);
                } catch (e) {
                    console.error('Error parsing booking:', e);
                }
            }
        }
        return bookings;
    }

    // filtering trips by client last name and ID
    function filterTripsByClient(bookings, lastName, clientId) {
        return bookings.filter(booking => 
            booking.travellers.some(traveller => 
                traveller.lastName.toLowerCase() === lastName.toLowerCase() &&
                traveller.officialId === clientId
            )
        );
    }

    // sorting trips by current/future and past (with YYYY-MM-DD format strings in Eastern time):
    function sortTrips(bookings) {
        function getDateStrInTimeZone(timeZone) {
            const now = new Date();
            const parts = new Intl.DateTimeFormat('en-US', { timeZone, year: 'numeric', month: '2-digit', day: '2-digit' }).formatToParts(now);
            const year = parts.find(p => p.type === 'year').value;
            const month = parts.find(p => p.type === 'month').value;
            const day = parts.find(p => p.type === 'day').value;
            return `${year}-${month}-${day}`;
        }
        const todayStr = getDateStrInTimeZone('America/New_York');
        const currentAndFutureTrips = [];
        const pastTrips = [];
        bookings.forEach(booking => {
            const td = booking.trip && booking.trip.trip_date ? booking.trip.trip_date : null;
            if (td < todayStr) {
                pastTrips.push(booking);
            } else {
                currentAndFutureTrips.push(booking);
            }
        });

        return {
            current: currentAndFutureTrips.sort((a, b) => 0),
            past: pastTrips.sort((a, b) => 0)
        };
    }

    // displaying trip
    function createTripHTML(booking) {
        return `
            <div class="trip-card">
                <h4>${booking.trip.departure_city} → ${booking.trip.arrival_city}</h4>
                <p>Trip Date: ${booking.trip.trip_date}</p>
                <p>Departure: ${booking.trip.departure_time}</p>
                <p>Arrival: ${booking.trip.arrival_time}</p>
                <p>Duration: ${booking.trip.trip_time} hours</p>
                <p>Booking ID: ${booking.bookingId}</p>
                <p>Travelers: ${booking.travellers.map(t => 
                    `${t.firstName} ${t.lastName} (${t.class} class)`).join(', ')}</p>
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

    // hndle form submission:
    clientSearchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const lastName = document.getElementById('client-lastname').value;
        const clientId = document.getElementById('client-id').value;

        const allBookings = getAllBookings();
        const clientBookings = filterTripsByClient(allBookings, lastName, clientId);
        const sortedTrips = sortTrips(clientBookings);
        
        displayTrips(sortedTrips);
    });
});
