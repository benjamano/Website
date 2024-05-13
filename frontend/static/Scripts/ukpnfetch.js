document.addEventListener("DOMContentLoaded", function() {
    const fetchfaultButton = document.getElementById("fetchButton");

    fetchfaultButton.addEventListener("click", function() {

        fetchfaultDataFromServer(mode="fault");
    });

    fetchlctButton.addEventListener("click", function(){

        fetchlctDataFromServer(mode="lct");

    });
});

function fetchfaultDataFromServer() {
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

function handleFaultData(data, mode) {
    console.log('Received fault data:', data);

    if (mode == "fault") {

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
    else if (mode == "lct"){
        //Low Carbon Tech
        console.log("Todo")
    }
}

function fetchlctDataFromServer() {
    fetch('/getlctdata')
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Failed to fetch fault data');
            }
        })
        .then(data => {
            handlelctFaultData(data);
        })
        .catch(error => {
            console.error('Error fetching fault data:', error);
        });
}