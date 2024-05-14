

function fetchAndHandleLctData() {
    fetchlctDataFromServer().then(data => {
        console.log('Fetched LCT Data:', data);
        localStorage.setItem('lctData', JSON.stringify(data));
    }).catch(error => {
        console.error('Error in fetching LCT data:', error);
    });
}

fetchAndHandleLctData();