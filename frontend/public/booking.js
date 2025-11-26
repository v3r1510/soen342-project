// take thee selected trip data:
const selectedTrip = JSON.parse(localStorage.getItem('selectedTrip'));

if (!selectedTrip) {
    alert('No trip selected. Redirecting to search...');
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
            populateAgeSelect(`age-${travellerCount}`); // (age select for the next added traveller)
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

    // generate a unique ticket number and trip ID
    function generateTicketNumber() {
    return `TKT${Date.now()}${Math.floor(Math.random() * 1000)}`;
    }

    // to confirm booking, save booking data to localStorage to be able to view in My Trips:
    bookingForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const travellers = [];

        for (let i = 1; i <= travellerCount; i++) {
            const traveller = {
                firstName: document.getElementById(`firstName-${i}`).value,
                lastName: document.getElementById(`lastName-${i}`).value,
                age: document.getElementById(`age-${i}`).value,
                officialId: document.getElementById(`officialid-${i}`).value,
                class: document.getElementById(`class-${i}`).value,
                ticketNumber: generateTicketNumber(),
            };
            travellers.push(traveller);
        }

        const bookingData = {
            trip: Object.assign({}, selectedTrip, {
                // store only the travel date as a string (YYYY-MM-DD)
                trip_date: document.getElementById('trip-date').value
            }),
            travellers: travellers,
            totalTravellers: travellerCount,
            bookingId: generateTicketNumber()
        };

        //unique key to store booking:
        const bookingKey = `booking_${bookingData.bookingId}`;
        localStorage.setItem(bookingKey, JSON.stringify(bookingData));

        window.location.href = 'profile.html';
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