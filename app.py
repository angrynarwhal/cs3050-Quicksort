from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)

# Store steps of the QuickSort algorithm for frontend
steps = []

def quicksort(arr):
    """Recursive QuickSort implementation that logs steps."""
    quicksort_helper(arr, 0, len(arr) - 1)

def quicksort_helper(arr, low, high):
    if low < high:
        pivot_index = partition(arr, low, high)
        quicksort_helper(arr, low, pivot_index - 1)
        quicksort_helper(arr, pivot_index + 1, high)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            steps.append({"arr": arr.copy(), "low": low, "high": high, "pivot": pivot, "i": i, "j": j})
    arr[i+1], arr[high] = arr[high], arr[i+1]
    steps.append({"arr": arr.copy(), "low": low, "high": high, "pivot": pivot, "i": i+1, "j": high})
    return i + 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quicksort')
def quicksort_data():
    global steps
    arr = [random.randint(1, 100) for _ in range(20)]  # Example array
    steps = []  # Reset steps
    quicksort(arr)  # Perform QuickSort and log steps
    return jsonify(steps)

if __name__ == "__main__":
    app.run(debug=True, port=5002)