document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('birth-info-form').addEventListener('submit', function(e) {
      e.preventDefault(); // Prevents the default form submission

      // Gather data from the form
      const birthInfo = {
          name: this.querySelector('[name="name"]').value,
          birth_date: this.querySelector('[name="birth_date"]').value,
          birth_time: this.querySelector('[name="birth_time"]').value,
          location: this.querySelector('[name="location"]').value
      };
      console.log(birthInfo)

      // Perform the AJAX request
      fetch('/charts/api/chart-data/', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCSRFToken() // Include CSRF token
          },
          body: JSON.stringify(birthInfo),
      })
      .then(response => response.json())
      .then(chartData => {
          renderChart(chartData); // Function to render the chart
      })
      .catch(error => console.error('Error fetching chart data:', error));
  });
});

function getCSRFToken() {
  return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function renderChart(chartData) {
    // Assuming chartData is the object containing all the necessary chart info
    // Use a charting library to render the chart inside the 'natal-chart-container' div
    const ctx = document.getElementById('natal-chart-container').getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line', // or 'bar', 'pie', etc., depending on your data
        data: {
            labels: chartData.positions.map(position => position.label),
            datasets: [{
                label: 'Planetary Positions',
                data: chartData.positions.map(position => position.value),
                // other chart options...
            }]
        },
        options: {
            // chart options...
        }
    });
}
