// wordcloud.js

function generateWordCloud(wordFrequencyData) {
    // Convert the word frequency data to an array of objects
    console.log(wordFrequencyData);
    var wordsArray = Object.entries(wordFrequencyData).map(([word, frequency]) => ({ word, frequency }));

    // Set up the dimensions for the word cloud
    var width = 800;
    var height = 400;

    // Create a scale for the font size based on word frequency
    var fontSizeScale = d3.scaleLinear()
        .domain([0, d3.max(wordsArray, d => d.frequency)])
        .range([10, 50]); // Adjust the range based on your preference

    // Generate the word cloud layout
    var layout = d3.layout.cloud()
        .size([width, height])
        .words(wordsArray)
        .padding(5)
        .rotate(() => Math.random() > 0.5 ? 90 : 0) // Random rotation
        .fontSize(d => fontSizeScale(d.frequency))
        .on("end", draw);

    // Select the container element for the word cloud
    var container = d3.select("#word-cloud");

    // Start the layout
    layout.start();

    // Function to draw the word cloud
    function draw(words) {
        container.append("svg")
            .attr("width", width)
            .attr("height", height)
            .append("g")
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")
            .selectAll("text")
            .data(words)
            .enter().append("text")
            .style("font-size", d => d.size + "px")
            .style("fill", "steelblue") // Adjust the color based on your preference
            .attr("text-anchor", "middle")
            .attr("transform", d => "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")")
            .text(d => d.word);
    }
}

// Call the function with the headlines from Flask
generateWordCloud(wordFrequencyData);