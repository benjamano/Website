console.log("Hello from turbines.js", lctData);
console.log(faultData);

let localLctData = "";

function fetchAndStoreLctData() {
    if (window.fetchlctDataFromServer) {
        window.fetchlctDataFromServer()
            .then(data => {
                localLctData = data;
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