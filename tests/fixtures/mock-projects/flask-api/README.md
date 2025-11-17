# Flask REST API - Simple Todo App

A simple REST API built with Flask for managing todos.

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### 1. Install Flask and dependencies

```bash
pip install flask flask-cors
```

### 2. Create the application

Create a file named `app.py`:

```python
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

todos = []

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    todo = request.json
    todos.append(todo)
    return jsonify(todo), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### 3. Run the application

```bash
python app.py
```

### 4. Test the API

In another terminal, test the endpoints:

```bash
# Get all todos
curl http://localhost:5000/todos

# Add a todo
curl -X POST http://localhost:5000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Test todo", "completed": false}'
```

You should see the todo in the response!

## Verification

The API should be running on `http://localhost:5000` and responding to requests.

