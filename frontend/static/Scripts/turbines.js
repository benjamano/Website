let lctData = "";

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
            lctData = data;
            console.log('Fetched fault data:', lctData);
        })
        .catch(error => {
            console.error('Error fetching fault data:', error);
        });
}

