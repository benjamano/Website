document.addEventListener("DOMContentLoaded", function() {
    const fetchButton = document.getElementById("fetchButton");

    fetchButton.addEventListener("click", function() {

        fetchDataFromServer();
    });
});

function fetchDataFromServer() {
    fetch('/getfaultdata')
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Failed to fetch fault data');
            }
        })
        .then(data => {
            handleFaultData(data);
        })
        .catch(error => {
            console.error('Error fetching fault data:', error);
        });
}

function handleFaultData(data) {
    console.log('Received fault data:', data);
    
    const creationDateTime = data.creationdatetime;
    console.log('Creation Date Time:', creationDateTime);
}

window.onload = fetchDataFromServer();
