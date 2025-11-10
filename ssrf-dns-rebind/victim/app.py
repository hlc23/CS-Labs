import socket
import ipaddress
from urllib.parse import urlparse
import requests
from flask import Flask, request, render_template, jsonify

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

def is_private_host(hostname):
    try:
        ip = socket.gethostbyname(hostname)
        return ipaddress.ip_address(ip).is_private
    except Exception:
        return False

@app.route('/fetch')
def fetch():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'missing url param'}), 400

    parsed = urlparse(url)
    hostname = parsed.hostname
    if not hostname:
        return jsonify({'error': 'invalid url'}), 400

    # Single DNS check (vulnerable pattern if DNS can change after this)
    if is_private_host(hostname):
        return jsonify({'error': 'blocked - private host'}), 403

    # Do the HTTP request using requests (this will do a fresh DNS resolution)
    try:
        resp = requests.get(url, timeout=5)
        return (resp.text, resp.status_code)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
