document.addEventListener("DOMContentLoaded", function() {
    const fetchButton = document.getElementById("fetchButton");

    fetchButton.addEventListener("click", function() {
        const url = "https://ukpowernetworks.opendatasoft.com/api/explore/v2.1/catalog/datasets/ukpn-live-faults/records?limit=20";
        const apikey = "2444be3184703156aa82afb58a6e9d1cdbe7e1b75b588d3329637c24";

        const headers = {
            "Content-Type": "application/json",
            "Authorization": `Apikey ${apikey}`
        };

        fetch(url, { headers })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error(`Failed to retrieve data. Status code: ${response.status}`);
                }
            })
            .then(data => {
                const total_count = data.total_count;
                const results = data.results;

                console.log("Total count:", total_count);
                console.log("Results:");
                console.log(results.length);
                results.forEach(record => {
                    console.log("-----------------------------------------------------------\n");
                    console.log(`Power Cut Type: ${record.powercuttype}`);
                    const postcodes = record.postcodesaffected.split(";");
                    console.log("Post Codes effected:");
                    postcodes.forEach(postcode => {
                        console.log(postcode);
                    });
                    console.log(`Description: ${record.incidentcategorycustomerfriendlydescription}\n\n`);
                });
            })
            .catch(error => {
                console.error(error.message);
            });
    });
});
