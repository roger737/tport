from flask import Flask, request, render_template
import sqlite3
import os

app = Flask(__name__)

DATABASE = os.path.join('instance', 'labs.db')


def init_db():
    if not os.path.exists('instance'):
        os.makedirs('instance')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    conn.commit()
    if c.execute('SELECT COUNT(*) FROM users').fetchone()[0] == 0:
        c.execute("INSERT INTO users (username, password) VALUES ('admin','password')")
        conn.commit()
    conn.close()


@app.route('/')
def index():
    labs = [
        {'name': 'SQL Injection', 'endpoint': 'sqli'},
        {'name': 'Cross-Site Scripting', 'endpoint': 'xss'},
        # Additional labs can be added here
    ]
    return render_template('index.html', labs=labs)


@app.route('/lab/sqli', methods=['GET', 'POST'])
def lab_sqli():
    level = request.args.get('level', '1')
    msg = ''
    if request.method == 'POST':
        username = request.form.get('username', '')
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        query = "SELECT * FROM users WHERE username = '%s'" % username  # vulnerable to SQL injection
        try:
            user = c.execute(query).fetchone()
            if user:
                msg = f"Welcome {user[1]}"
            else:
                msg = "User not found"
        except Exception as e:
            msg = str(e)
        conn.close()
    return render_template('sqli.html', message=msg, level=level)


@app.route('/lab/xss', methods=['GET', 'POST'])
def lab_xss():
    level = request.args.get('level', '1')
    comment = ''
    if request.method == 'POST':
        comment = request.form.get('comment', '')
    return render_template('xss.html', comment=comment, level=level)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
