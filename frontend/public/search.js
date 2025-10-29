function sendHttpRequest() {
    const departureCity = document.getElementById('departureCity').value;
    // You can add more fields as needed
    fetch('http://127.0.0.1:5000/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ departureCity })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Search results:', data);
        // Optionally display results in the page
        // document.querySelector('.container').innerHTML = JSON.stringify(data.routes);
    })
    .catch(error => {
        console.error('Search failed:', error);
    });
}