#!/bin/bash
# Golden script for Flask API installation and testing
# This is the CORRECT way to test the Flask API documentation

set -e

echo "=== Flask REST API Test Script ==="

# Step 1: Install dependencies
echo "Installing Flask and dependencies..."
pip install flask flask-cors

# Step 2: Create the application file
echo "Creating app.py..."
cat > app.py << 'EOF'
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
EOF

# Step 3: Start the Flask app in background
echo "Starting Flask application..."
python app.py &
FLASK_PID=$!

# Wait for Flask to start
sleep 3

# Step 4: Test the API endpoints
echo "Testing API endpoints..."

# Test GET /todos
echo "Testing GET /todos..."
curl -s http://localhost:5000/todos || (kill $FLASK_PID; exit 1)

# Test POST /todos
echo "Testing POST /todos..."
RESPONSE=$(curl -s -X POST http://localhost:5000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Test todo", "completed": false}')

# Verify response contains the todo
if echo "$RESPONSE" | grep -q "Test todo"; then
    echo "✅ API test successful!"
else
    echo "❌ API test failed!"
    kill $FLASK_PID
    exit 1
fi

# Cleanup
kill $FLASK_PID
rm -f app.py

echo "=== All tests passed! ==="

