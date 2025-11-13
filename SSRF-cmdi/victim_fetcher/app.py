from flask import Flask, render_template, request
import requests
from urllib.parse import urlparse
import ipaddress

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/fetch")
def fetch():
    url = request.args.get("url", "").strip()
    if not url:
        return "Missing 'url' parameter", 400

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return "Only http/https allowed", 400
    if not parsed.netloc:
        return "Invalid URL host", 400

    host = (parsed.hostname or "").lower()

    blocked_hosts = {"localhost", "admin"}
    if host in blocked_hosts:
        return "Blocked host", 400

    try:
        ip = ipaddress.ip_address(host.strip("[]"))
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            return "Blocked private/loopback address", 400
    except ValueError:
        pass

    try:
        r = requests.get(url, timeout=5, allow_redirects=True)
        ct = r.headers.get("Content-Type", "application/octet-stream")
        return (r.content, r.status_code, {"Content-Type": ct})
    except Exception as e:
        return (f"Error fetching {url}: {e}", 500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
