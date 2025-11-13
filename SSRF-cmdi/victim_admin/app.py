from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)


@app.route("/")
def root():
    return "Admin service. Try /admin/ping?host=example.com", 200


@app.route("/admin/ping")
def admin_ping():
    host = request.args.get("host")
    if not host:
        return jsonify({"error": "missing host"}), 400
    cmd = f"ping -c 1 {host}"
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        return (
            f"Command: {cmd}\nExit: {res.returncode}\n--- stdout ---\n{res.stdout}\n--- stderr ---\n{res.stderr}\n",
            200,
            {"Content-Type": "text/plain; charset=utf-8"},
        )
    except subprocess.TimeoutExpired:
        return jsonify({"error": "command timeout"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
