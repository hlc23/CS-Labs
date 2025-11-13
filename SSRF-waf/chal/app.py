from flask import Flask, request, render_template, abort, send_file
from urllib.parse import urlparse
from config import flag1, flag2
import requests

app = Flask(__name__)


@app.route("/mkreq1", methods=["GET"])
def make_request1():
    url = request.args.get("url")
    if urlparse(url).hostname in ["localhost", "127.0.0.1", "::1"]:
        return "badhacker"
    return requests.get(url, verify=False, timeout=2).text


@app.route("/internal-only1")
def internal_only1():
    if request.remote_addr != "127.0.0.1":
        abort(403)
    return flag1


@app.route("/mkreq2", methods=["GET"])
def make_request2():
    url = request.args.get("url")
    if not urlparse(url).hostname.startswith("httpbin.dev"):
        return "badhacker"
    return requests.get(url, verify=False, timeout=2).text


@app.route("/internal-only2")
def internal_only2():
    if request.remote_addr != "127.0.0.1":
        abort(403)
    return flag2


@app.route("/")
def home():
    if request.args.get("debug"):
        return send_file("app.py")
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)