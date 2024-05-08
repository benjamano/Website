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
                return response.json();
            } else {
                throw new Error('Failed to fetch fault data');
            }
        })
        .then(data => {
            // Call another function to handle the fetched data
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
        const ul = document.createElement('ul');
        data.forEach(record => {
            const li = document.createElement('li');
            li.textContent = `Power Cut Type: ${record.powercuttype}, Post Codes Affected: ${record.postcodesaffected}`;
            ul.appendChild(li);
        });
        resultsContainer.appendChild(ul);
    } else {
        resultsContainer.textContent = 'No fault data available.';
    }
}

// Call the function to fetch data when the page loads
window.onload = fetchDataFromServer();
