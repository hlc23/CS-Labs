from flask import Flask, request, render_template, redirect, url_for, make_response
import secrets

app = Flask(__name__)

sessions = {}  # Simple in-memory session store for demo purposes

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Simple authentication: any username/password combination works
        session_id = secrets.token_hex(16)
        sessions[session_id] = username
        resp = make_response(redirect(url_for('profile')))
        resp.set_cookie('sessionid', session_id)
        return resp
    return render_template('login.html')

@app.route('/profile')
def profile():
    session_id = request.cookies.get('sessionid')
    if session_id not in sessions:
        return redirect(url_for('login'))
    username = sessions[session_id]
    return render_template('profile.html', username=username)

@app.route('/search')
def search():
    q = request.args.get('q', '')
    return render_template('search.html', q=q)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)