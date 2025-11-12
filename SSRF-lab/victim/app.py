from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch')
def fetch():
    url = request.args.get('url')
    if not url:
        return "No URL provided", 400
    try:
        response = requests.get(url, timeout=5)
        return response.text
    except Exception as e:
        return str(e), 500

@app.route('/secret')
def secret():
    if request.remote_addr != '127.0.0.1':
        return "Access denied", 403
    return "You find the secret data!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)