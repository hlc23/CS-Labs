from flask import Flask, request, session, render_template, redirect, url_for
import secrets

app = Flask(__name__)
app.secret_key = 'secret_key_for_demo'

# In-memory user storage
users = {'victim': 'password', 'hacker': 'cake'}
balances = {'victim': 1000, 'hacker': 100}

def generate_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    return session['csrf_token']

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        return 'Invalid credentials.'
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', balance=balances[session['username']], csrf_token=generate_csrf_token())

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if 'username' not in session:
        return redirect(url_for('index'))

    token = None
    if request.method == 'POST':
        token = request.form.get('csrf_token')
    elif request.method == 'GET':
        token = request.args.get('csrf_token')
    
    if token and token != session.get('csrf_token'):
        return 'Invalid CSRF token.'
    
    amount = int(request.form.get('amount', request.args.get('amount', 0)))
    to_account = request.form.get('to_account', request.args.get('to_account', ''))
    if amount <= 0 or to_account == '':
        return 'Invalid transfer details.'
    if balances[session['username']] >= amount:
        balances[session['username']] -= amount
        balances[to_account] = balances.get(to_account, 0) + amount
        return f'Transferred ${amount} to {to_account}. New balance: ${balances[session["username"]]}'
    return 'Insufficient funds.'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
