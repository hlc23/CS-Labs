from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch-attack')
def fetch_attack():
    return render_template('fetch_attack.html')

@app.route('/form-attack')
def form_attack():
    return render_template('form_attack.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)