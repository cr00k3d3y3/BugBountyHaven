from flask import Flask, request, render_template, redirect, url_for, g, make_response
from markupsafe import Markup
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'ultrasecret'
DATABASE = 'data.db'

def initialize_db():
    if not Path(DATABASE).exists():
        db = sqlite3.connect(DATABASE)
        db.executescript(open('schema.sql').read())
        db.close()

initialize_db()

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

def log_attempt(endpoint, ip, payload):
    db = get_db()
    db.execute("INSERT INTO logs (endpoint, ip, payload) VALUES (?, ?, ?)", (endpoint, ip, payload))
    db.commit()

messages = []


@app.route('/')
def xss_home():
    return render_template('index.html')


@app.route('/reflected')
def reflected():
    msg = request.args.get("msg", "")
    output = Markup(msg)
    flag = ''
    hint = 'Try ?msg=<script>alert(1)</script>'
    username = request.cookies.get('auth') or 'anonymous'

    if "<script" in msg.lower():
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM submissions WHERE flag_value = ? AND username = ?", ('FLAG{reflected_xss_triggered}', username))
        if not cur.fetchone():
            cur.execute("INSERT INTO submissions (username, flag_value, challenge_name) VALUES (?, ?, ?)",
                        (username, 'FLAG{reflected_xss_triggered}', 'Reflected XSS'))
            db.commit()
        flag = '🎉 FLAG{reflected_xss_triggered}'
    return render_template("reflected.html", msg=output, hint=hint, flag=flag)

@app.route('/reflected_tutorial')
def reflected_tutorial():
    return render_template('reflected_tutorial.html')

@app.route('/stored', methods=['GET', 'POST'])
def stored():
    username = request.cookies.get('auth') or 'anonymous'
    hint = 'Post <script>fetch("/steal?flag=FLAG")</script>'
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

@app.route('/stored_tutorial')
def stored_tutorial():
    return render_template('stored_tutorial.html')


@app.route('/dom')
def dom():
    username = request.cookies.get('auth') or 'anonymous'
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM submissions WHERE flag_value = ? AND username = ?", ('FLAG{dom_xss_triggered}', username))
    flag = ''
    if not cur.fetchone():
        # simulate automatic trigger, as if JS was injected successfully
        cur.execute("INSERT INTO submissions (username, flag_value, challenge_name) VALUES (?, ?, ?)",
                    (username, 'FLAG{dom_xss_triggered}', 'DOM XSS'))
        db.commit()
        flag = '🎉 FLAG{dom_xss_triggered}'
    return render_template("dom.html", flag=flag)

@app.route('/dom_tutorial')
def dom_tutorial():
    return render_template('dom_tutorial.html')

@app.route('/steal')
def steal():
    flag = request.args.get('flag')
    log_attempt('/steal', request.remote_addr, flag or 'EMPTY')
    return '', 204

@app.route('/submit_flag', methods=['GET', 'POST'])
def submit_flag():
    result = ''
    if request.method == 'POST':
        username = request.form['username'].strip()
        submitted_flag = request.form['flag'].strip()

        db = get_db()
        cur = db.cursor()

        cur.execute("SELECT challenge_name FROM flags WHERE flag_value = ?", (submitted_flag,))
        row = cur.fetchone()

        if row:
            challenge = row[0]
            cur.execute("SELECT 1 FROM submissions WHERE flag_value = ? AND username = ?", (submitted_flag, username))
            if cur.fetchone():
                result = "❗️ Flag already submitted."
            else:
                cur.execute(
                    "INSERT INTO submissions (username, flag_value, challenge_name, stars) VALUES (?, ?, ?, ?)",
                    (username, submitted_flag, challenge, 1)
                )
                cur.execute(
                    "INSERT INTO logs (endpoint, ip, payload) VALUES (?, ?, ?)",
                    ('/submit_flag', request.remote_addr, f'{username}:{submitted_flag}')
                )
                db.commit()
                result = f"✅ Flag accepted for challenge: {challenge}"
        else:
            result = "❌ Invalid flag."

    return render_template('submit_flag.html', result=result)

@app.route('/scoreboard')
def scoreboard():
    cur = get_db().cursor()
    cur.execute("SELECT username, challenge_name, timestamp FROM submissions ORDER BY timestamp DESC")
    rows = cur.fetchall()
    return render_template('scoreboard.html', rows=rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
