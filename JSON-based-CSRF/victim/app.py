from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow all origins for demonstration of CORS misconfig

@app.route('/api/data', methods=['POST'])
def api_data():
    if request.headers.get('Content-Type') == 'application/json':
        data = request.json
        return jsonify({"message": "Data received", "data": data}), 200
    return jsonify({"error": "Invalid Content-Type"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)