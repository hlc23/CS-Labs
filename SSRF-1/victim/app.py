from flask import Flask, request, render_template, abort, send_file
from urllib.parse import urlparse
from config import flag
import requests

app = Flask(__name__)


@app.route("/mkreq", methods=["GET"])
def make_request():
    url = request.args.get("url")
    if not urlparse(url).hostname.startswith("httpbin.dev"):
        return "badhacker"
    return requests.get(url, verify=False, timeout=2).text


@app.route("/internal-only")
def internal_only():
    if request.remote_addr != "127.0.0.1":
        abort(403)
    return flag


@app.route("/")
def home():
    if request.args.get("debug"):
        return send_file("app.py")
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)