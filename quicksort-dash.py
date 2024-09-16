import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import random
import threading

# Global variables to track the sorting steps and colors
steps = []
colors = []
sorted_steps = False

# Function to perform QuickSort and store the sorting steps and colors
def quicksort(arr):
    global steps, colors
    quicksort_helper(arr, 0, len(arr) - 1, ['skyblue'] * len(arr))  # Initial color setup

def quicksort_helper(arr, low, high, color_map):
    if low < high:
        pi = partition(arr, low, high, color_map)
        steps.append((list(arr), list(color_map)))  # Log current state of array and colors
        quicksort_helper(arr, low, pi - 1, color_map)
        quicksort_helper(arr, pi + 1, high, color_map)

def partition(arr, low, high, color_map):
    pivot = arr[high]
    i = low - 1
    color_map[high] = 'red'  # Mark the pivot
    for j in range(low, high):
        color_map[j] = 'skyblue'  # Left partition
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
        steps.append((list(arr), list(color_map)))  # Log after each swap
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    color_map[i + 1] = 'green'  # Mark as sorted
    color_map[high] = 'lightgray'  # Restore pivot color after swap
    steps.append((list(arr), list(color_map)))  # Log final step of partitioning
    return i + 1

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the Dash app
app.layout = html.Div([
    html.H1("QuickSort Visualization with Dash and Plotly"),
    html.H3("Pivot: Red (to highlight the current pivot"),
	html.H3("Left Partition: Skyblue or Blue."),
	html.H3("Right Partition: Light gray."),
	html.H3("Fully Sorted: Green."),
    dcc.Graph(id='graph'),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0)  # Update every 1 second
])

# Callback to update the graph based on sorting steps
@app.callback(
    Output('graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n_intervals):
    global sorted_steps
    if n_intervals < len(steps):
        # Show the current step of sorting
        current_array, current_colors = steps[n_intervals]
        fig = create_bar_chart(current_array, current_colors)
        return fig
    elif not sorted_steps:
        # Once sorting is complete, display the sorted array
        sorted_steps = True
        return create_bar_chart(steps[-1][0], steps[-1][1])
    else:
        return dash.no_update

# Function to create the bar chart with color mapping
def create_bar_chart(array, colors):
    fig = go.Figure(go.Bar(
        x=list(range(len(array))),
        y=array,
        marker=dict(color=colors)  # Apply colors to bars
    ))

    fig.update_layout(
        xaxis_title="Index",
        yaxis_title="Value",
        yaxis=dict(range=[0, max(array) + 10]),
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    return fig

# Start the sorting algorithm in a separate thread
def run_quick_sort():
    global steps
    arr = random.sample(range(1, 100), 20)  # Example array with random elements
    steps = []  # Reset the steps
    quicksort(arr)  # Perform the sorting

# Start the sorting algorithm in a separate thread
threading.Thread(target=run_quick_sort).start()

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True, port=5002)