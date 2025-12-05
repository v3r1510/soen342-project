// take thee selected trip data:
const selectedTrip = JSON.parse(localStorage.getItem('selectedTrip'));

if (!selectedTrip) {
    // alert('No trip selected. Redirecting to search...');
    window.location.href = 'index.html';
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('trip-summary').innerHTML = `
        <h2>Selected Connection:</h2>
        <p><strong>Route:</strong> ${selectedTrip.departure_city} → ${selectedTrip.arrival_city}</p>
        <p><strong>Departure:</strong> ${selectedTrip.departure_time}</p>
        <p><strong>Arrival:</strong> ${selectedTrip.arrival_time}</p>
        <p><strong>Duration:</strong> ${selectedTrip.trip_time} hours</p>
        <p><strong>First Class:</strong> €${selectedTrip.first_class_rate}</p>
        <p><strong>Second Class:</strong> €${selectedTrip.second_class_rate}</p>
    `;

    let travellerCount = 1;
    const maxTravellers = 4; // current requirement for use case (family of 4)

    const addTravellerBtn = document.getElementById('add-traveller');
    const removeTravellerBtn = document.getElementById('remove-traveller');
    const travellersContainer = document.getElementById('travellers-container');
    const bookingForm = document.getElementById('booking-form');

    // add traveller:
    addTravellerBtn.addEventListener('click', () => {
        if (travellerCount < maxTravellers) {
            travellerCount++;
            const newTravellerForm = createTravellerForm(travellerCount);
            travellersContainer.appendChild(newTravellerForm);
            populateAgeSelect(`age-${travellerCount}`);
            removeTravellerBtn.disabled = false;
            if (travellerCount === maxTravellers) {
                addTravellerBtn.disabled = true;
            }
        }
    });

    // remove traveller:
    removeTravellerBtn.addEventListener('click', () => {
        if (travellerCount > 1) {
            travellersContainer.removeChild(travellersContainer.lastChild);
            travellerCount--;
            addTravellerBtn.disabled = false;

            if (travellerCount === 1) {
                removeTravellerBtn.disabled = true;
            }
        }
    });

    // helper to show all age select options for each traveller id:
    function populateAgeSelect(selectId) {
        const ageSelect = document.getElementById(selectId);
        if (!ageSelect) return;

        ageSelect.innerHTML = '';
        const placeholder = document.createElement('option');
        placeholder.value = '';
        placeholder.textContent = 'Select Age';
        ageSelect.appendChild(placeholder);

        for (let i = 1; i <= 100; i++) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = i;
            ageSelect.appendChild(option);
        }
    }


    populateAgeSelect('age-1');

    //form to send to backend
    bookingForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Get the trip date from the form
        const tripDate = document.getElementById('trip-date').value;

        if (!tripDate) {
            alert('Please select a trip date.');
            return;
        }

        // Collect all traveller data from html form
        const travellers = [];
        for (let i = 1; i <= travellerCount; i++) {
            const firstName = document.getElementById(`firstName-${i}`).value;
            const lastName = document.getElementById(`lastName-${i}`).value;
            const age = parseInt(document.getElementById(`age-${i}`).value);
            const officialId = document.getElementById(`officialid-${i}`).value;
            const travelClass = document.getElementById(`class-${i}`).value;

            const traveller = {
                name: `${firstName} ${lastName}`,
                age: age,
                client_id: officialId,
                travel_class: travelClass,
                // Store additional details for frontend use
                firstName: firstName,
                lastName: lastName
            };
            travellers.push(traveller);
        }

        // Prepare booking info for backend (database link)
        const routeId = selectedTrip.route_id;

        if (!routeId) {
            console.error('Selected trip object:', selectedTrip);
            alert('Error: Route ID is missing. Please select a trip again.');
            window.location.href = 'index.html';
            return;
        }

        const bookingPayload = {
            route_id: routeId,
            trip_date: tripDate,
            travelers: travellers
        };

        // Show loading state
        const submitBtn = bookingForm.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.textContent;
        submitBtn.textContent = 'Booking...';
        submitBtn.disabled = true;

        try {
            // Send booking request to backend
            const response = await fetch('http://127.0.0.1:5000/book-trip', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(bookingPayload)
            });

            const data = await response.json();

            if (response.ok && data.success) {
                // Booking successful
                alert('Booking confirmed successfully!');
                //cached trip
                const cachedBooking = {
                    trip: Object.assign({}, selectedTrip, {
                        trip_date: tripDate,
                    }),
                    travellers: travellers,
                    totalTravellers: travellerCount,
                    timestamp: new Date().toISOString()
                };


                // Clear selected trip from localStorage
                localStorage.removeItem('selectedTrip');

                // Redirect to profile page
                window.location.href = 'profile.html';
            } else {
                // Booking failed
                throw new Error(data.error || 'Booking failed');
            }
        } catch (error) {
            console.error('Booking error:', error);
            alert(`Failed to complete booking: ${error.message}\nPlease try again.`);

            // Restore button state
            submitBtn.textContent = originalBtnText;
            submitBtn.disabled = false;
        }
    });
});

// creating a new traveller form
function createTravellerForm(travellerId) {
    const div = document.createElement('div');
    div.className = 'traveller-form';
    div.dataset.travellerId = travellerId;

    div.innerHTML = `
        <h3>Traveller ${travellerId}</h3>
        <label for="firstName-${travellerId}">First Name:</label>
        <input type="text" id="firstName-${travellerId}" name="firstName-${travellerId}" required>

        <label for="lastName-${travellerId}">Last Name:</label>
        <input type="text" id="lastName-${travellerId}" name="lastName-${travellerId}" required>

        <label for="age-${travellerId}">Age:</label>
        <select id="age-${travellerId}" name="age-${travellerId}" required>
            <option value="">Select Age</option>
        </select>

        <label for="officialid-${travellerId}">Official ID:</label>
        <input type="text" id="officialid-${travellerId}" name="officialid-${travellerId}" required>

        <label for="class-${travellerId}">Travel Class:</label>
        <select id="class-${travellerId}" name="class-${travellerId}" required>
            <option value="">Select Class</option>
            <option value="second">Second Class</option>
            <option value="first">First Class</option>
        </select>
    `;

    return div;
}