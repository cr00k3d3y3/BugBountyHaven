# Final Cleaned SQLiPlayground/app.py
from flask import Flask, request, render_template, g, make_response, redirect, url_for
import sqlite3, time
from pathlib import Path
import jwt
# RS256 to HS256 Key Confusion Attack Integration
# SQLiPlayground/app.py (add below existing imports)
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from jwt import encode as jwt_encode, decode as jwt_decode, algorithms




JWT_SECRET = 'wrong-secret'  # intentionally insecure
JWT_ALGORITHM = 'HS256'

app = Flask(__name__)
app.secret_key = 'ultrasecret'
DATABASE = 'data.db'

PRIVATE_KEY_PEM = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7LmbHZ36jxoD0
83sVXQVbN4Tv1YBkWEk2qv+LN/LG/FyYoosUDapUZR9Un8JKLW2rbSToQjafTymj
wL2ttzpwJeR6wdI7jW7U8XZ7gCGC5u+qLRbwQGK7bOxg1U37pXEZ4wiNpp1xns/t
cz2XOIsLPd6zKJFZrvzWiiTwC2eDstzcYTqD94apQPjdTz2c35KGU8+IjtKbC+ra
1LDjt8j+DgbN/7glYnwa+U4+MZx3Elngen0vq4RjYXJsvvyjqmJPc1O4JWRrmBeB
WTPJrn1YDsu5BuWnU2HX/295U9QlSRURUHWgfCFHBCYRrPVrnsrI2yil2ZycmqTl
PN7fV7/PAgMBAAECggEAMRgBgwllEMWOqzB1Nuw37G3KYzEnRKpXQYxmC/i3p3Mn
Qi1XtwHCi/Id3o8sYVI68nxk8rnzI6Oas0VpOnfVTvbRT1Uos8/rotRWFBxOLcwu
Tf8XhhoNC0WNVfR8SKVi3bxLUQPDRbq2pHvWSqRc66zljS31uYUI8ag3+fGzy7mZ
sPE428tqjjHzP85lRSFo367ULgpK+84lbzgJwLU885GbzNrgL/QjHb7/7TBWt4Xf
J2lOVDRtpEhtSvFmk1wgiIrdAJuGUqkxcct90N5LF8ncuSTTS/EwfjYl33BZ31OL
M2frM7irwzS0AbkGzDiiXFHgBiHO/FwffBt7bi5MOQKBgQDuL2u3XgStKy9OFSRR
s16SNmg4SDhInZOUnHq+pSj557J2TnS6+n9zowvqhZbNolPiy9FbnL1r6Z6QRdSI
ETdHz0BkK8UiwhFR8XsiKm9txRSPcNnP2+XDmJ29dT2cQ30InrG2A6yGmuyuY7ve
oRHUclSeFlYQf7m4QL4rosc82wKBgQDJLmXEAhET4TiAiIyLrdTZog+a0BDSyW5e
px5IyvTkbqbBREXLVlcraOX2clHNelF+/+wjxUIJRiAXdt4Ko9WfuczVnLiPQNWK
YFvkjLt+llBx4fSiF6yjz8q4pkz54uDJfQspieX/FZanFAyiP3TIJ5u6rjnp0Y/V
PekmKGsBHQKBgQDeWMBKVecxrL2lO5FC/5nKDiYuXCTGjOsm8QiYjd95ovRzAnxv
y8ZMsak/DeQgJGgAsNnIlsIxSc4uyjFDsCaVz4BBwqZt8xJuF2omE80fgLnXybZb
FuEfPYoLQbX4+Ptwn4wv6LAWm+tURGAtzNizJOOfDCTdlA5QVYfxfixVvwKBgCyn
AatZkhTJflL4+8jc0ktjrvb7i2BdmQOlMBGUCnrRHG31C1CwXzShWbkzcnia14/K
mczusVOBnwnWNj5CUt3azV30JPqWt065SGwX2F2mW0CLmFKJ0qWhLyuArcEg3Cec
e2fC1auiTQfUaWFxmCf8spHirbP58WSxExiHDAj5AoGAFySo7pXE5gRVfPhRYSPj
ffkiuDO3Hxc2B7o6t55Tc1gMAbNciiXNebqoRC/C6Ix+4+ivJ2WYEo9Cr5ySH/Tb
iE0W929wxeywRCbizxpG/na4kOuVwMkIrOENEU3mFO9zM9odS5QuFsjy8L2f9o/T
pl+oR58CEHV+zHtuBNmTyos=
-----END PRIVATE KEY-----""".strip()


PUBLIC_KEY_PEM = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuy5mx2d+o8aA9PN7FV0F
WzeE79WAZFhJNqr/izfyxvxcmKKLFA2qVGUfVJ/CSi1tq20k6EI2n08po8C9rbc6
cCXkesHSO41u1PF2e4Ahgubvqi0W8EBiu2zsYNVN+6VxGeMIjaadcZ7P7XM9lziL
Cz3esyiRWa781ook8Atng7Lc3GE6g/eGqUD43U89nN+ShlPPiI7Smwvq2tSw47fI
/g4Gzf+4JWJ8GvlOPjGcdxJZ4Hp9L6uEY2FybL78o6piT3NTuCVka5gXgVkzya59
WA7LuQblp1Nh1/9veVPUJUkVEVB1oHwhRwQmEaz1a57KyNsopdmcnJqk5Tze31e/
zwIDAQAB
-----END PUBLIC KEY-----""".strip()

# DB Initialization

def initialize_db():
    if not Path(DATABASE).exists():
        db = sqlite3.connect(DATABASE)
        with open('schema.sql') as f:
            db.executescript(f.read())
        db.close()

initialize_db()

# DB Connection

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

# Log Requests

def log_attempt(endpoint, ip, payload):
    db = get_db()
    db.execute("INSERT INTO logs (endpoint, ip, payload) VALUES (?, ?, ?)", (endpoint, ip, payload))
    db.commit()

# Routes

@app.route('/home')
def sqli_home():
    return render_template('index.html')

@app.route('/')
def redirect_home():
    return redirect('/home')


@app.route('/classic', methods=['GET', 'POST'])
def classic():
    result, flag = '', ''
    hint = "Try injecting ' OR 1=1-- to bypass."
    if request.method == 'POST':
        name = request.form['name']
        log_attempt('/classic', request.remote_addr, name)
        query = f"SELECT * FROM users WHERE username = '{name}'"
        try:
            cur = get_db().cursor()
            cur.execute(query)
            data = cur.fetchall()
            result = data
            if any('admin' in str(row) for row in data):
                flag = '🎉 FLAG{classic_sqli_exploited}'
        except Exception as e:
            result = f"❌ Error: {e}"
    return render_template('classic.html', result=result, flag=flag, hint=hint)

@app.route('/union', methods=['GET', 'POST'])
def union():
    result, flag = '', ''
    hint = "Try UNION SELECT 1, 'admin'--"
    if request.method == 'POST':
        name = request.form['name']
        log_attempt('/union', request.remote_addr, name)
        query = f"SELECT id, username FROM users WHERE username = '{name}'"
        try:
            cur = get_db().cursor()
            cur.execute(query)
            result = cur.fetchall()
            if any('admin' in str(row) for row in result):
                flag = '🎉 FLAG{union_sqli_extracted}'
        except Exception as e:
            result = f"❌ Error: {e}"
    return render_template('union.html', result=result, flag=flag, hint=hint)

@app.route('/union_tutorial')
def union_tutorial():
    return render_template('union_tutorial.html')


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    result = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cur = get_db().cursor()
        cur.execute(query)
        user = cur.fetchone()
        if user:
            resp = make_response(render_template('auth.html', result=f"Welcome, {user[1]}!"))
            resp.set_cookie('auth', user[1])
            resp.set_cookie('role', user[4])
            return resp
        else:
            result = "Invalid credentials"
    return render_template('auth.html', result=result)

from datetime import datetime

# Add to app.py (email alert config and review logging setup)
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

EMAIL_SENDER = 'alert@bbhlab.local'
EMAIL_RECEIVER = 'ded3y3@proton.me'
SMTP_SERVER = 'localhost'

# Email alert function
def send_alert(subject, body):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER

        with smtplib.SMTP(SMTP_SERVER) as server:
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
    except Exception as e:
        print(f"[!] Failed to send email: {e}")

@app.route('/moderate', methods=['GET', 'POST'])
def moderate():
    if request.cookies.get('role') != 'admin':
        return "Access Denied"

    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        comment_id = request.form.get('id')
        action = request.form.get('action')
        mod = request.cookies.get('auth') or 'admin'
        new_status = 'approved' if action == 'approve' else 'flagged'
        cur.execute("UPDATE feedback SET status = ?, moderated_by = ? WHERE id = ?", (new_status, mod, comment_id))
        db.commit()

    cur.execute("SELECT id, comment, status, moderated_by FROM feedback ORDER BY id DESC")
    comments = cur.fetchall()
    return render_template("moderate.html", comments=comments)


@app.route('/reviewlog')
def review_log():
    cur = get_db().cursor()
    cur.execute("SELECT id, endpoint, ip, payload, timestamp FROM logs WHERE endpoint='/moderate' ORDER BY timestamp DESC")
    entries = cur.fetchall()
    return render_template('reviewlog.html', entries=entries)



@app.route('/scoreboard')
def scoreboard():
    cur = get_db().cursor()
    cur.execute("SELECT username, challenge_name, timestamp FROM submissions ORDER BY timestamp DESC")
    rows = cur.fetchall()
    return render_template('scoreboard.html', rows=rows)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    db = get_db()
    cur = db.cursor()
    
    if request.method == 'POST':
        comment = request.form.get('comment', '').strip()
        if comment:
            cur.execute("INSERT INTO feedback (comment) VALUES (?)", (comment,))
            db.commit()

    cur.execute("SELECT id, comment FROM feedback ORDER BY id DESC")
    rows = cur.fetchall()
    return render_template('feedback.html', rows=rows)


@app.route('/logs')
def view_logs():
    cur = get_db().cursor()
    cur.execute("SELECT endpoint, ip, payload, timestamp FROM logs ORDER BY timestamp DESC")
    rows = cur.fetchall()
    return render_template('logs.html', rows=rows)


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



@app.route('/reset_scoreboard', methods=['POST'])
def reset_scoreboard():
    if request.cookies.get('role') != 'admin':
        return "Access Denied", 403
    db = get_db()
    db.execute("DELETE FROM submissions")
    db.commit()
    return redirect(url_for('scoreboard'))


@app.route('/leak', methods=['GET', 'POST'])
def leak():
    result, flag = '', ''
    hint = "Leak SESSIONID=admin_ID by trying admin, guest, etc."
    if request.method == 'POST':
        user = request.form['user']
        log_attempt('/leak', request.remote_addr, user)
        query = f"SELECT * FROM users WHERE username = '{user}'"
        cur = get_db().cursor()
        try:
            cur.execute(query)
            row = cur.fetchone()
            if row:
                result = f"SESSIONID=admin_{row[0]}"
                if row[1] == 'admin':
                    flag = '🎉 FLAG{session_hijack}'
            else:
                result = "❌ No user found."
        except Exception as e:
            result = f"❌ Error: {e}"
    return render_template('leak.html', result=result, hint=hint, flag=flag)

@app.route('/admin')
def admin():
    if request.cookies.get('role') == 'admin':
        return render_template('flag.html', flag='FLAG{admin_area_access}')
    return "Access Denied"

@app.route('/campaign')
def campaign():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM challenges")
    challenges = cur.fetchall()

    username = request.cookies.get('auth') or 'anonymous'
    cur.execute("SELECT flag_value, stars FROM submissions WHERE username = ?", (username,))
    found = {row[0].strip(): row[1] for row in cur.fetchall()}

    progress = []
    for ch in challenges:
        flag_value = ch[4].strip()  # Ensure no invisible characters
        print("Found flags:", found.keys())
        print("Challenge flag:", repr(flag_value))

        stars = found.get(flag_value, 0)
        status = '✅ Solved' if stars else '❌ Unsolved'
        progress.append((ch[1], ch[2], ch[3], status, ch[5], stars))

    return render_template("campaign.html", progress=progress)



@app.route('/blind', methods=['GET', 'POST'])
def blind():
    result = ''
    hint = 'Try comparing known true and false conditions like: AND 1=1-- vs AND 1=0--'
    if request.method == 'POST':
        name = request.form['name']
        log_attempt('/blind', request.remote_addr, name)
        query = f"SELECT * FROM users WHERE username = '{name}'"
        try:
            cur = get_db().cursor()
            cur.execute(query)
            data = cur.fetchall()
            result = "✅ User exists (True)" if data else "❌ No match (False)"
        except:
            result = "❌ Query Error"
    return render_template('blind.html', result=result, hint=hint)

@app.route('/time', methods=['GET', 'POST'])
def time_based():
    result = ''
    hint = 'Try sleep() inside a SQL condition like: OR IF(1=1, SLEEP(5), 0)--'
    if request.method == 'POST':
        name = request.form['name']
        log_attempt('/time', request.remote_addr, name)
        if 'sleep' in name.lower():
            time.sleep(5)
            result = "⏱ Delay detected — likely injectable"
        else:
            result = f"Processed input: {name}"
    return render_template('time.html', result=result, hint=hint)

@app.route('/stacked', methods=['GET', 'POST'])
def stacked():
    results = []
    hint = 'Try: SELECT 1; UPDATE users SET role=\'admin\' WHERE username=\'guest\';'
    flag = ''
    if request.method == 'POST':
        raw_input = request.form['sql']
        log_attempt('/stacked', request.remote_addr, raw_input)
        queries = [q.strip() for q in raw_input.strip().split(';') if q.strip()]
        db = get_db()
        cur = db.cursor()
        for q in queries:
            try:
                cur.execute(q)
                db.commit()
                try:
                    data = cur.fetchall()
                    results.append(data)
                    if any('admin' in str(d) for d in data):
                        flag = '🎉 FLAG{stacked_query_executed}'
                except:
                    results.append("✅ Executed")
            except Exception as e:
                results.append(f"❌ Error: {e}")
    return render_template('stacked.html', result=results, hint=hint, flag=flag)


@app.route('/robots.txt')
def robots():
    return (
        "User-agent: *\n"
        "Disallow: /admin/\n"
        "Disallow: /backup.zip\n"
        "Disallow: /debug.php\n"
        "Disallow: /admin/config.php\n"
        "Disallow: /secret_dashboard\n",
        200,
        {'Content-Type': 'text/plain'}
    )

@app.route('/secret_dashboard')
def secret_dashboard():
    username = request.cookies.get('auth') or 'anonymous'
    cur = get_db().cursor()
    cur.execute("SELECT * FROM submissions WHERE username = ? AND flag_value = ?", (username, 'FLAG{found_hidden_admin_panel}'))
    if not cur.fetchone():
        cur.execute("INSERT INTO submissions (username, flag_value, challenge_name) VALUES (?, ?, ?)",
                    (username, 'FLAG{found_hidden_admin_panel}', 'Recon - Hidden Admin Panel'))
        get_db().commit()
    return render_template('secret.html')

@app.route('/.git/HEAD')
def git_head():
    log_attempt('/.git/HEAD', request.remote_addr, 'git enum')
    return "ref: refs/heads/main", 200, {'Content-Type': 'text/plain'}

@app.route('/git-config')
def git_config():
    flag = ''
    hint = 'Check this page for secrets often exposed by developers.'
    content = """
    [core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
    [remote "origin"]
        url = https://github.com/example/bbh-lab.git
        fetch = +refs/heads/*:refs/remotes/origin/*
    [user]
        name = devadmin
        email = admin@example.com
    """

    # simulate flag drop if accessed
    user = request.cookies.get('auth') or 'anonymous'
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM submissions WHERE flag_value = ? AND username = ?", ('FLAG{exposed_git_config}', user))
    if not cur.fetchone():
        cur.execute("INSERT INTO submissions (username, flag_value, challenge_name) VALUES (?, ?, ?)",
                    (user, 'FLAG{exposed_git_config}', 'Exposed Git Config'))
        db.commit()
        flag = '🎉 FLAG{exposed_git_config}'

    return render_template("git_config.html", content=content, flag=flag, hint=hint)

@app.route('/.env')
def dot_env():
    content = """APP_ENV=production
APP_DEBUG=false
DB_HOST=localhost
DB_USER=admin
DB_PASS=supersecret
SECRET_KEY=FLAG{env_file_exposed}"""
    return app.response_class(content, mimetype='text/plain')

@app.route('/.git/config')
def git_config_route():
    content = """[core]
    repositoryformatversion = 0
    filemode = true
    bare = false
    logallrefupdates = true
[remote "origin"]
    url = https://github.com/example/target-repo.git
[branch "main"]
    remote = origin
    merge = refs/heads/main

# FLAG{git_config_leakage_detected}
"""
    return app.response_class(content, mimetype='text/plain')

@app.route('/admin-panel', methods=['GET', 'POST'])
def admin_panel_exposed():
    if request.cookies.get('role') == 'admin':
        flag = '🎯 FLAG{admin_interface_exposed}'
        return render_template('flag.html', flag=flag)

    return "🔐 Forbidden: Admins only. This page should not be exposed.", 403

@app.route('/backup.zip')
def backup_zip():
    username = request.cookies.get('auth') or 'anonymous'
    flag_value = 'FLAG{backup_archive_exposed}'
    challenge_name = 'Exposed Backup File'

    log_attempt('/backup.zip', request.remote_addr, 'attempted zip file access')

    cur = get_db().cursor()
    cur.execute("SELECT * FROM submissions WHERE username = ? AND flag_value = ?", (username, flag_value))
    if not cur.fetchone():
        cur.execute("INSERT INTO submissions (username, flag_value, challenge_name) VALUES (?, ?, ?)",
                    (username, flag_value, challenge_name))
        get_db().commit()

    return '''
        <h2>📦 Simulated Backup Archive: backup.zip</h2>
        <p><strong>Contents:</strong></p>
        <ul>
          <li>index.php</li>
          <li>config.php</li>
          <li>data.db</li>
          <li>.env</li>
        </ul>
        <p><code>🎉 FLAG{backup_archive_exposed}</code></p>
    '''

# JWT: Login using HS256 (no password required)
@app.route('/jwt_login', methods=['GET', 'POST'])
def jwt_login():
    token = None
    if request.method == 'POST':
        username = request.form['username']
        role = 'admin' if username == 'admin' else 'user'
        token = jwt.encode({"username": username, "role": role}, JWT_SECRET, algorithm="HS256")
        resp = make_response(render_template('jwt_login.html', token=token))
        resp.set_cookie('jwt', token)
        return resp
    return render_template('jwt_login.html')

# JWT: Admin panel that validates HS256 token
@app.route('/jwt_admin')
def jwt_admin():
    token = request.cookies.get('jwt')
    if not token:
        return "❌ Missing token"
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if decoded.get("role") == "admin":
            return render_template('flag.html', flag="FLAG{jwt_token_tampering}")
        else:
            return "Access denied"
    except Exception as e:
        return f"❌ Invalid token: {str(e)}"

# JWT None Algorithm Injection
@app.route('/jwt_none', methods=['GET', 'POST'])
def jwt_none():
    if request.method == 'POST':
        username = request.form['username']
        token = jwt.encode({'user': username, 'role': 'user'}, JWT_SECRET, algorithm='HS256')
        resp = make_response(render_template('jwt_none.html', token=token))
        resp.set_cookie('jwt_none', token)
        return resp
    return render_template('jwt_none.html')


@app.route('/jwt_admin_none')
def jwt_admin_none():
    token = request.cookies.get('jwt_none')
    if not token:
        return "❌ No token provided"

    try:
        # Normally verifies signature, but we allow alg: none bypass
        unverified = jwt.decode(token, options={"verify_signature": False}, algorithms=["none", "HS256"])
        if unverified.get('role') == 'admin':
            # Check submission
            username = unverified.get('user', 'anonymous')
            cur = get_db().cursor()
            cur.execute("SELECT * FROM submissions WHERE username = ? AND flag_value = ?", (username, 'FLAG{jwt_none_alg_bypass}'))
            if not cur.fetchone():
                cur.execute("INSERT INTO submissions (username, flag_value, challenge_name) VALUES (?, ?, ?)",
                            (username, 'FLAG{jwt_none_alg_bypass}', 'JWT None Algorithm Abuse'))
                get_db().commit()
            return render_template('flag.html', flag='FLAG{jwt_none_alg_bypass}')
        else:
            return "Access denied"
    except Exception as e:
        return f"❌ Token invalid: {str(e)}"


# JWT RS256 Key Confusion
@app.route('/jwt_confusion', methods=['GET'])
def jwt_confusion():
    return render_template('jwt_confusion.html', pubkey=PUBLIC_KEY_PEM.decode())

@app.route('/jwt_rs_admin')
def jwt_rs_admin():
    token = request.cookies.get('jwt')
    if not token:
        return "❌ Missing token"

    try:
        decoded = jwt.decode(token, PUBLIC_KEY_PEM, algorithms=["RS256", "HS256"])
        if decoded.get("role") == "admin":
            user = decoded.get("user", "anonymous")
            db = get_db()
            cur = db.cursor()
            flag_value = 'FLAG{jwt_rs256_hs256_confusion}'
            cur.execute("SELECT * FROM submissions WHERE username = ? AND flag_value = ?", (user, flag_value))
            if not cur.fetchone():
                cur.execute("INSERT INTO submissions (username, flag_value, challenge_name) VALUES (?, ?, ?)",
                            (user, flag_value, "JWT Key Confusion"))
                db.commit()
            return render_template("flag.html", flag=flag_value)
        return "❌ Not admin"
    except Exception as e:
        return f"❌ Invalid token: {e}"
    

@app.route('/jwt_key')
def jwt_key_disclosure():
    return app.response_class(PUBLIC_KEY_PEM, mimetype='text/plain')


@app.route('/jwt_admin_key')
def jwt_admin_key_access():
    token = request.cookies.get('jwt')
    if not token:
        return "❌ No token found in cookie"

    try:
        decoded = jwt_decode(token, PUBLIC_KEY_PEM, algorithms=["RS256", "HS256"])
        if decoded.get("role") == "admin":
            return render_template('flag.html', flag="FLAG{jwt_key_confusion_rs256_to_hs256}")
        else:
            return "🔒 Not admin"
    except Exception as e:
        return f"❌ Invalid token: {str(e)}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
