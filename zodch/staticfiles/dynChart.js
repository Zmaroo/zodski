document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('birth-info-form').addEventListener('submit', function (e) {
        e.preventDefault(); // Prevents the default form submission

        // Gather data from the form
        const birthInfo = {
            name: this.querySelector('[name="name"]').value,
            birth_date: this.querySelector('[name="birth_date"]').value,
            birth_time: this.querySelector('[name="birth_time"]').value,
            location: this.querySelector('[name="location"]').value
        };
        console.log(birthInfo);

        // Perform the AJAX request
        console.log("Making AJAX request");
        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify(birthInfo),
        })
        .then(response => response.json()) // Convert the response to a JavaScript object
        .then(data => {
            console.log("Received data:", data);
            renderNatalChart(data); // Call renderNatalChart with the object
        })
        .catch(error => {
            console.error('Error fetching chart data:', error);
        });
    });
});

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function renderNatalChart(zodiac_counts) {
    // TODO: Update rendering logic to incorporate aspects into the natal chart
    console.log("Rendering natal chart with data:", zodiac_counts);

    // Assume zodiac_counts is now an object and not an array
    const labels = Object.keys(zodiac_counts);
    const planetData = labels.map(label => zodiac_counts[label].planets);
    const houseData = labels.map(label => zodiac_counts[label].houses);
    const ascData = labels.map(label => zodiac_counts[label].ascendant);
    const mcData = labels.map(label => zodiac_counts[label].midheaven);


    // Create datasets for each aspect
    const datasets = [
        {
            label: 'Planets',
            data: planetData,
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1,
            pointRadius: 3
        },
        {
            label: 'Houses',
            data: houseData,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1,
            pointRadius: 3
        },
        {
            label: 'Ascendant',
            data: ascData,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
            pointRadius: 3
        },
        {
            label: 'Midheaven',
            data: mcData,
            backgroundColor: 'rgba(153, 102, 255, 0.2)',
            borderColor: 'rgba(153, 102, 255, 1)',
            borderWidth: 1,
            pointRadius: 3
        }
    ];

    // Get the context of the canvas element
    const ctx = document.getElementById('natal-chart-container').getContext('2d');

    // Create the radar chart
    const chart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: datasets
        ,
        {
            label: 'Aspects',
            data: labels.map(label => zodiac_counts[label].aspects),
            backgroundColor: 'rgba(255, 206, 86, 0.2)',
            borderColor: 'rgba(255, 206, 86, 1)',
            borderWidth: 1,
            pointRadius: 3
        }        },
        options: {
            scale: {
                ticks: {
                    beginAtZero: true
                }
            },
            elements: {
                line: {
                    tension: 0.2 // Smooths the line
                }
            }
        }
    });
}

