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

# Function to perform HeapSort and store sorting steps and colors
def heap_sort(arr):
    global steps, colors
    n = len(arr)

    # Build a max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, ['blue'] * n)  # Initially all elements are part of the heap

    # Extract elements from heap
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # Swap the current largest (root) with the end of the array
        color_map = ['green' if x >= i else 'blue' for x in range(n)]  # Mark sorted elements as green
        color_map[i] = 'red'  # Mark the current extracted element
        steps.append((list(arr), list(color_map)))  # Log the state and colors after swap
        heapify(arr, i, 0, color_map)  # Heapify the reduced heap

# Function to heapify a subtree rooted at index i
def heapify(arr, n, i, color_map):
    largest = i  # Initialize largest as root
    left = 2 * i + 1  # Left child
    right = 2 * i + 2  # Right child

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # Swap
        steps.append((list(arr), list(color_map)))  # Log the state after each swap
        heapify(arr, n, largest, color_map)  # Recursively heapify the affected subtree

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the Dash app
app.layout = html.Div([
    html.H1("HeapSort Visualization with Dash and Plotly"),
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
def run_heap_sort():
    global steps
    arr = random.sample(range(1, 100), 20)  # Example array with random elements
    steps = []  # Reset the steps
    heap_sort(arr)  # Perform the sorting

# Start the sorting algorithm in a separate thread
threading.Thread(target=run_heap_sort).start()

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True, port=5002)