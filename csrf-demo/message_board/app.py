from flask import Flask, request, session, redirect, url_for, render_template

app = Flask(__name__)
app.secret_key = 'secret_key_for_demo'

users = {}  # In-memory user storage: username -> password
messages = []  # List of messages

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('board'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username and password and username not in users:
            users[username] = password
            session['username'] = username
            return redirect(url_for('board'))
        return 'Registration failed. Username may already exist.'
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            session['username'] = username
            return redirect(url_for('board'))
        return 'Invalid credentials.'
    return render_template('login.html')

@app.route('/board')
def board():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('board.html', messages=messages, username=session['username'])

@app.route('/post', methods=['POST'])
def post():
    if 'username' not in session:
        return redirect(url_for('index'))
    message = request.form['message']
    if message:
        messages.append(f"{session['username']}: {message}")
    return redirect(url_for('board'))

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'username' in session:
        username = session['username']
        if username in users:
            del users[username]
        session.pop('username', None)
        # Remove user's messages
        global messages
        messages = [m for m in messages if not m.startswith(username + ':')]
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)