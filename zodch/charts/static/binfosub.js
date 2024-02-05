document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('birth-info-form').addEventListener('submit', function(e) {
        e.preventDefault(); // Prevents the default form submission

        // Gather data from the form
        const formData = new FormData(this);

        // Perform the AJAX request
        fetch('/path/to/your/view/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken') // CSRF token for Django
            },
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response data
            console.log(data);
            displayChartResult(data); // Function to display the result
        })
        .catch(error => console.error('Error:', error));
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function displayChartResult(data) {
    // Update the page with the chart data
    const resultDiv = document.getElementById('chart-result');
    // Format and display data. This is a basic example.
    resultDiv.textContent = JSON.stringify(data, null, 2);
}
