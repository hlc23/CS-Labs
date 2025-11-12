import os
from flask import Flask, render_template

app = Flask(__name__)

# Victim base URL (can be overridden via env VICTIM_BASE_URL)
VICTIM = "http://localhost:6080"


@app.route("/")
def index():
    return render_template("index.html", victim=VICTIM)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
