function updateSentimentGraph(jsonData) {
    // Parse the JSON data
    var data = JSON.parse(jsonData);

    // Create an object to store unique entries for each date
    var uniqueEntries = {};

    // Iterate through the data and keep only the first entry for each date
    data.forEach(entry => {
        var date = entry.date.split(' ')[0]; // Extracting the date part
        if (!uniqueEntries[date]) {
            uniqueEntries[date] = entry;
        }
    });

    // Extract dates and sentiments from the unique entries
    var dates = Object.keys(uniqueEntries);
    var sentiments = dates.map(date => parseFloat(uniqueEntries[date].sentiment));

    // Create a Chart.js chart
    var ctx = document.getElementById('sentimentChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Sentiment over Time',
                data: sentiments,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                fill: false
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}