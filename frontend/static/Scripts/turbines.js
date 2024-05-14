console.log("Hello from turbines.js", lctData);
console.log(faultdata);

let localLctData = "";

function fetchAndStoreLctData() {
    if (window.fetchlctDataFromServer) {
        window.fetchlctDataFromServer()
            .then(data => {
                localLctData = data; // Store the fetched data locally
                console.log('Stored LCT Data:', localLctData);
            })
            .catch(error => {
                console.error('Error fetching LCT data:', error);
            });
    } else {
        console.error('fetchlctDataFromServer is not defined');
    }
}

fetchAndStoreLctData();