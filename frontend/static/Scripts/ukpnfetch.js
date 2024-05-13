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

    for (const record of data) {
        const creationDateTime = record.creationdatetime;
        const mainMessage = record.mainmessage;
        const customersaffected = record.nocustomeraffected;
        const powerCutType = record.powercuttype;
        const noCallsReported = record.nocallsreported;
        const postCodesAffected = record.postcodesaffected;
        console.log('Record:', creationDateTime, mainMessage, customersaffected, powerCutType, noCallsReported, postCodesAffected);
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const fetchButton = document.getElementById("fetchButton");

    fetchButton.addEventListener("click", function() {
        fetchDataFromServer();
    });

    fetchDataFromServer();
});
