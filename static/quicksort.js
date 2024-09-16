const svg = d3.select("svg");
const width = +svg.attr("width");
const height = +svg.attr("height");
let duration = 500;

// Fixed margin for the bars
const margin = 50;

// Function to render the bars with dynamic spacing between divided partitions
function renderBars(data, low, high, depth, isFinalStep = false) {
    const totalElements = data.length;
    const availableWidth = width - 2 * margin;  // Total width available for bars and partitions

    // Calculate partition space, limited to ensure bars fit in the canvas
    const maxPartitionSpace = Math.min((availableWidth / totalElements) * 2, (depth + 1) * 50);
    const partitionSpace = isFinalStep ? 0 : maxPartitionSpace;  // Add space only during sorting

    // Dynamically calculate the maximum possible bar width
    const barWidth = Math.min(availableWidth / totalElements - 5, 30);  // Cap width at 30px

    // X scale for positioning bars and ensuring no overflow
    const x = d3.scaleBand()
        .domain(d3.range(0, totalElements))  // Cover all elements in the array
        .range([margin, width - margin])  // Keep bars within the canvas
        .padding(0.1);  // Padding between bars within the same partition

    // Y scale for bar heights
    const y = d3.scaleLinear()
        .domain([0, d3.max(data)])
        .range([height, 0]);

    // Bind data to the bars
    const bars = svg.selectAll(".bar")
        .data(data, (d, i) => i);

    // Enter phase: Add new bars
    bars.enter()
        .append("rect")
        .attr("class", "bar")
        .attr("x", (d, i) => {
            // Apply partition space between the divided partitions
            if (i >= low && i <= high) {
                return x(i) + partitionSpace / 2;  // Extra space for current partition
            } else {
                return x(i);  // Normal spacing for bars outside the current partition
            }
        })
        .attr("y", d => y(d))
        .attr("height", d => height - y(d))
        .attr("width", barWidth);  // Use dynamic bar width

    // Update phase: Animate the transition of bars
    bars.transition()
        .duration(duration)
        .attr("x", (d, i) => {
            // Adjust x position during sorting to add partition space dynamically
            if (i >= low && i <= high) {
                return x(i) + partitionSpace / 2;  // Extra space for current partition
            } else {
                return x(i);  // Normal spacing for bars outside the current partition
            }
        })
        .attr("y", d => y(d))
        .attr("height", d => height - y(d))
        .attr("width", barWidth);  // Use dynamic bar width

    // Exit phase: Remove old bars
    bars.exit().remove();
}

// Function to update the visualization at each sorting step
function updateVisualization(step, depth, isFinalStep = false) {
    const data = step.arr;
    const low = step.low;
    const high = step.high;

    // Render the bars and add partition spacing based on depth
    renderBars(data, low, high, depth, isFinalStep);

    // Highlight the pivot element
    const bars = svg.selectAll(".bar")
        .data(data, (d, i) => i);

    bars.classed("pivot", (d, i) => i === step.j);
}

// Function to start the QuickSort visualization
function runQuickSortVisualization() {
    d3.json('/quicksort').then(steps => {
        let i = 0;
        let depth = 0;
        const interval = setInterval(() => {
            if (i < steps.length) {
                const currentStep = steps[i];
                depth = Math.floor(Math.log2(i + 1));  // Adjust depth dynamically
                // Check if this is the last step (final sorted array)
                const isFinalStep = i === steps.length - 1;
                updateVisualization(currentStep, depth, isFinalStep);
                i++;
            } else {
                clearInterval(interval);
            }
        }, duration);
    });
}

runQuickSortVisualization();