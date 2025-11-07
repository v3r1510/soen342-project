// take thee selected trip data:
const selectedTrip = JSON.parse(localStorage.getItem('selectedTrip'));

if (!selectedTrip) {
    alert('No trip selected. Redirecting to search...');
    window.location.href = 'index.html';
}

document.addEventListener('DOMContentLoaded', () => {
    // displaying chosen connection
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

    // add traveller
    addTravellerBtn.addEventListener('click', () => {
        if (travellerCount < maxTravellers) {
            travellerCount++;
            const newTravellerForm = createTravellerForm(travellerCount);
            travellersContainer.appendChild(newTravellerForm);
            removeTravellerBtn.disabled = false;
            
            if (travellerCount === maxTravellers) {
                addTravellerBtn.disabled = true;
            }
        }
    });

    // remove traveller
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

    const ageSelect = document.getElementById('age-1');
    for (let i = 1; i <= 100; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = i;
        ageSelect.appendChild(option);
    }

    // generate a unique ticket number and trip ID
    function generateTicketNumber() {
    return `TKT${Date.now()}${Math.floor(Math.random() * 1000)}`;
    }

    // to confirm booking, save booking data to localStorage for the next step
    bookingForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const travellers = [];

        for (let i = 1; i <= travellerCount; i++) {
            const traveller = {
                firstName: document.getElementById(`firstName-${i}`).value,
                lastName: document.getElementById(`lastName-${i}`).value,
                age: document.getElementById(`age-${i}`).value,
                class: document.getElementById(`class-${i}`).value,
                ticketNumber: generateTicketNumber(),
            };
            travellers.push(traveller);
        }

        const bookingData = {
            trip: selectedTrip,
            travellers: travellers,
            totalTravellers: travellerCount,
            bookingId: generateTicketNumber()
        };

        localStorage.setItem('bookingData', JSON.stringify(bookingData));

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
        <label for="class-${travellerId}">Travel Class:</label>
        <select id="class-${travellerId}" name="class-${travellerId}" required>
            <option value="">Select Class</option>
            <option value="second">Second Class</option>
            <option value="first">First Class</option>
        </select>
    `;

    return div;
}