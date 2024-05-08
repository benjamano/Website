document.addEventListener("DOMContentLoaded", function() {
    const fetchButton = document.getElementById("fetchButton");

    fetchButton.addEventListener("click", function() {

        fetchDataFromServer();
    });
});

function fetchDataFromServer() {
    // Make a request to the Flask endpoint to fetch fault data
    fetch('/getfaultdata')
        .then(response => {
            if (response.ok) {
                return response.json(); // Parse the response as JSON
            } else {
                throw new Error('Failed to fetch fault data');
            }
        })
        .then(data => {
            // Data fetched successfully, handle it
            handleFaultData(data);
        })
        .catch(error => {
            console.error('Error fetching fault data:', error);
        });
}

// Function to handle the fetched fault data
function handleFaultData(data) {
    // Assuming data is an array of fault records
    console.log('Received fault data:', data);

    // Example: Display the data on the webpage
    const resultsContainer = document.getElementById('results-container');
    resultsContainer.innerHTML = ''; // Clear previous results

    if (data.length > 0) {
        data.forEach(record => {
            console.log(`Power Cut Type: ${record.powercuttype}, Post Codes Affected: ${record.postcodesaffected}`);
        });
    } else {
        console.log('No fault data available.');
    }
}

// Call the function to fetch data when the page loads
window.onload = fetchDataFromServer();
