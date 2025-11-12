from flask import Flask, request, jsonify

app = Flask(__name__)

# Example route
@app.route('/')
def home():
    return "Welcome to My Flask App!"

# Example route that echoes user input
@app.route('/echo', methods=['POST'])
def echo():
    data = request.get_json()
    message = data.get('message', 'No message provided')
    return jsonify({"echo": message})

# Simple vulnerable example for CodeQL testing (e.g., unsanitized input)
@app.route('/greet')
def greet():
    name = request.args.get('name', 'Guest')
    return f"Hello {name}"  # Potential XSS if used in HTML

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
