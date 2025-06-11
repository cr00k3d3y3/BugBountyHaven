from flask import Flask, request, render_template, send_file, redirect, url_for, g, make_response
import os
import sqlite3
from datetime import datetime
from pathlib import Path
import time

app = Flask(__name__)
app.secret_key = 'ultrasecret'
DATABASE = 'data.db'
UPLOAD_FOLDER = 'uploads'

# Ensure uploads directory exists
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

# DB Setup

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Logging for commands/flag triggers

def log_attempt(endpoint, ip, payload):
    db = get_db()
    db.execute("INSERT INTO logs (endpoint, ip, payload) VALUES (?, ?, ?)", (endpoint, ip, payload))
    db.commit()

# Routes

@app.route('/', methods=['GET', 'POST'])
def lfi_home():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "❌ No file uploaded"
        file = request.files['file']
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)
        return f"✅ Uploaded to: {filename}"
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "❌ No file uploaded"
    file = request.files['file']
    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filename)
    return f"✅ Uploaded to: {filename}"

@app.route('/view')
def view():
    page = request.args.get('page', '')
    if '..' in page or page.startswith('/') or page.startswith('\\'):
        return "❌ Invalid path"

    path = os.path.join(UPLOAD_FOLDER, page)
    if not os.path.exists(path):
        return "❌ File not found"

    if path.endswith('.txt'):
        return open(path).read()
    elif path.endswith('.php') and 'shell' in page:
        # Trigger flag for LFI Shell
        user = request.cookies.get('auth') or 'anonymous'
        db = get_db()
        cur = db.cursor()
        flag = 'FLAG{lfi_shell_triggered}'
        cur.execute("SELECT * FROM submissions WHERE flag_value = ? AND username = ?", (flag, user))
        if not cur.fetchone():
            cur.execute("INSERT INTO submissions (username, flag_value, challenge_name, stars) VALUES (?, ?, ?, ?)",
                        (user, flag, 'LFI - Shell Trigger', 1))
            db.commit()
        log_attempt('/view', request.remote_addr, f'LFI shell by {user}')
        return f"💣 Simulated shell execution for user: {user} — FLAG submitted"
    else:
        return f"📄 File included: {path}"

@app.route('/shell')
def shell():
    cmd = request.args.get('cmd', '')
    log_path = os.path.join('uploads', 'shell_logs.txt')
    os.makedirs('uploads', exist_ok=True)

    if cmd:
        with open(log_path, 'a') as log_file:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {cmd}\n")

        result = os.popen(cmd).read()

        # Trigger flag if command is successful (simulating reverse shell)
        if 'whoami' in cmd or 'id' in cmd:
            username = request.cookies.get('auth') or 'anonymous'
            flag_value = 'FLAG{reverse_shell_triggered}'
            cur = get_db().cursor()
            cur.execute("SELECT * FROM submissions WHERE username = ? AND flag_value = ?", (username, flag_value))
            if not cur.fetchone():
                cur.execute("INSERT INTO submissions (username, flag_value, challenge_name) VALUES (?, ?, ?)",
                            (username, flag_value, 'LFI Reverse Shell'))
                get_db().commit()
            result += f"\n\n🎉 {flag_value}"

        return f"<pre>{result}</pre>"

    return '''
        <h3>💣 Trigger Shell</h3>
        <form method="get">
            <input name="cmd" placeholder="Enter command">
            <input type="submit" value="Execute">
        </form>
    '''

@app.route('/shell_logs')
def shell_logs():
    try:
        with open('uploads/shell_logs.txt') as f:
            content = f.read()
    except FileNotFoundError:
        content = ''
    return render_template("shell_logs.html", logs=content)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
