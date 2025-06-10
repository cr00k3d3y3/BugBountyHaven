from flask import Flask, request, render_template, redirect, url_for, g
import sqlite3
from markupsafe import Markup
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'ultrasecret'
DATABASE = 'data.db'

# Auto-init DB

# DB and logger

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def log_attempt(endpoint, ip, payload):
    db = get_db()
    db.execute("INSERT INTO logs (endpoint, ip, payload) VALUES (?, ?, ?)", (endpoint, ip, payload))
    db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/reflected')
def reflected():
    msg = request.args.get("msg", "")
    output = Markup(msg)
    flag = ''
    hint = 'Try ?msg=<script>alert(1)</script>'
    if "<script" in msg.lower():
        flag = '🎉 FLAG{reflected_xss_triggered}'
    return render_template("reflected.html", msg=output, hint=hint, flag=flag)

@app.route('/stored', methods=['GET', 'POST'])
def stored():
    messages = []
    username = request.cookies.get('auth') or 'anonymous'
    hint = 'Try <script>fetch("/steal?flag=FLAG")</script>'
    flag = ''
    db = get_db()
    cur = db.cursor()
    if request.method == 'POST':
        val = request.form['msg']
        messages.append(Markup(val))
        log_attempt('/stored', request.remote_addr, val)
        if "<script" in val.lower():
            cur.execute("SELECT * FROM submissions WHERE flag_value = ? AND username = ?", ('FLAG{stored_xss_executed}', username))
            if not cur.fetchone():
                cur.execute("INSERT INTO submissions (username, flag_value, challenge_name) VALUES (?, ?, ?)",
                            (username, 'FLAG{stored_xss_executed}', 'Stored XSS'))
                db.commit()
        return redirect(url_for('stored'))
    cur.execute("SELECT * FROM submissions WHERE flag_value = ? AND username = ?", ('FLAG{stored_xss_executed}', username))
    if cur.fetchone():
        flag = '🎉 FLAG{stored_xss_executed}'
    return render_template("stored.html", messages=messages, hint=hint, flag=flag)

@app.route('/dom')
def dom():
    return render_template("dom.html")

@app.route('/steal')
def steal():
    flag = request.args.get('flag')
    print(f"🔥 Exfiltrated: {flag}")
    log_attempt('/steal', request.remote_addr, flag or 'EMPTY')
    return '', 204