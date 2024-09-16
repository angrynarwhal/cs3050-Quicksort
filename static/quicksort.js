const svg = d3.select("svg");
const width = +svg.attr("width");
const height = +svg.attr("height");
const barWidth = 40;
let duration = 500;

function renderBars(data) {
    const x = d3.scaleBand()
        .domain(d3.range(data.length))
        .range([0, width])
        .padding(0.1);

    const y = d3.scaleLinear()
        .domain([0, d3.max(data)])
        .range([height, 0]);

    // Bind data
    const bars = svg.selectAll(".bar")
        .data(data, (d, i) => i);

    // Enter phase
    bars.enter()
        .append("rect")
        .attr("class", "bar")
        .attr("x", (d, i) => x(i))
        .attr("y", d => y(d))
        .attr("height", d => height - y(d))
        .attr("width", x.bandwidth());

    // Update phase
    bars.transition()
        .duration(duration)
        .attr("x", (d, i) => x(i))
        .attr("y", d => y(d))
        .attr("height", d => height - y(d));

    // Exit phase
    bars.exit().remove();
}

function updateVisualization(step) {
    const data = step.arr;
    renderBars(data);
    
    // Highlight pivot element
    const bars = svg.selectAll(".bar")
        .data(data, (d, i) => i);

    bars.classed("pivot", (d, i) => i === step.j);
}

function runQuickSortVisualization() {
    d3.json('/quicksort').then(steps => {
        let i = 0;
        const interval = setInterval(() => {
            if (i < steps.length) {
                updateVisualization(steps[i]);
                i++;
            } else {
                clearInterval(interval);
            }
        }, duration);
    });
}

runQuickSortVisualization();