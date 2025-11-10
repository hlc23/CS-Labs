from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Use 0.0.0.0 so it's reachable inside containers/runners
    app.run(host='0.0.0.0', port=5000, debug=True)
