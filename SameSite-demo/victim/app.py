from flask import Flask, request, make_response, render_template, redirect, url_for
from datetime import timedelta

app = Flask(__name__)

# In-memory state for demo purposes
STATE = {
    "mode": "Lax"  # One of: "Lax", "Strict", "None"
}

COOKIE_NAME = "demo_session"


def get_cookie_settings():
    mode = STATE["mode"]
    # For SameSite=None, modern browsers require the cookie to be Secure and served over HTTPS
    secure = (mode == "None")
    samesite = mode  # Flask accepts 'Lax', 'Strict', or 'None'
    return samesite, secure


@app.route("/")
def index():
    mode = STATE["mode"]
    authed = (request.cookies.get(COOKIE_NAME) == "valid")
    return render_template("index.html", mode=mode, authed=authed)


@app.route("/set_mode/<mode>")
def set_mode(mode: str):
    normalized = mode.capitalize()
    if normalized not in {"Lax", "Strict", "None"}:
        return make_response(f"Invalid mode: {mode}", 400)
    STATE["mode"] = normalized
    # Update existing cookie with new settings if present
    if request.cookies.get(COOKIE_NAME):
        samesite, secure = get_cookie_settings()
        resp = make_response(redirect(url_for("index")))
        resp.set_cookie(
            COOKIE_NAME,
            "valid",
            max_age=int(timedelta(hours=1).total_seconds()),
            httponly=True,
            samesite=samesite,
            secure=secure,
        )
        return resp
    return redirect(url_for("index"))


@app.route("/login", methods=["POST"])  # Simulate login and set cookie
def login():
    samesite, secure = get_cookie_settings()
    resp = make_response(redirect(url_for("index")))
    resp.set_cookie(
        COOKIE_NAME,
        "valid",
        max_age=int(timedelta(hours=1).total_seconds()),
        httponly=True,
        samesite=samesite,
        secure=secure,
    )
    return resp


@app.route("/logout", methods=["POST"])  # Clear the cookie
def logout():
    resp = make_response(redirect(url_for("index")))
    resp.delete_cookie(COOKIE_NAME)
    return resp


@app.route("/transfer", methods=["GET", "POST"])  # Protected action
def transfer():
    if request.cookies.get(COOKIE_NAME) != "valid":
        return make_response("Not authenticated. Cookie wasn't sent.", 401)
    # Just a simple page indicating whether the request method worked
    return render_template("transfer.html", method=request.method)


@app.route("/pixel")  # Return 1x1 PNG only if authenticated
def pixel():
    import base64
    if request.cookies.get(COOKIE_NAME) != "valid":
        return make_response("Unauthorized", 401)
    # 1x1 transparent PNG
    png_b64 = (
        b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAA\n"
        b"AAC0lEQVR42mP8/x8AAwMCAO2yKpQAAAAASUVORK5CYII="
    )
    data = base64.b64decode(png_b64)
    resp = make_response(data)
    resp.headers["Content-Type"] = "image/png"
    return resp


if __name__ == "__main__":
    # Bind to 0.0.0.0 so Docker can expose it
    app.run(host="0.0.0.0", port=5000, debug=False)
