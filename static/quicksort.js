const svg = d3.select("svg");
const width = +svg.attr("width");
const height = +svg.attr("height");
let duration = 500;

// Fixed width for each bar and total width calculation
const barWidth = 40;
const margin = 50;  // margin for padding on both sides

// Function to render the bars with extra space between divided partitions
function renderBars(data, low, high, depth, isFinalStep = false) {
    // Total number of elements and available width for the entire array
    const totalElements = data.length;
    const availableWidth = width - 2 * margin;  // Leave some margin on the sides

    // Dynamic partition space, which grows based on the recursion depth
    const partitionSpace = isFinalStep ? 0 : (depth + 1) * 30;  // No space in the final step

    // X scale: Ensures all bars fit within the available space
    const x = d3.scaleBand()
        .domain(d3.range(0, totalElements))  // We ensure to cover all elements in the array
        .range([margin, availableWidth - margin])  // Keep bars within the canvas
        .padding(0.2);  // Padding between bars

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
            // Adjust x position based on partition spacing, no space in the final sorted step
            const adjustedX = i < low || i > high ? x(i) : x(i) + partitionSpace;
            return adjustedX;
        })
        .attr("y", d => y(d))
        .attr("height", d => height - y(d))
        .attr("width", x.bandwidth());

    // Update phase: Animate the transition of bars
    bars.transition()
        .duration(duration)
        .attr("x", (d, i) => {
            // Adjust x position based on partition spacing, no space in the final sorted step
            const adjustedX = i < low || i > high ? x(i) : x(i) + partitionSpace;
            return adjustedX;
        })
        .attr("y", d => y(d))
        .attr("height", d => height - y(d));

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