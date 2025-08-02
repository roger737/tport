import sqlite3
from flask import Blueprint, request, g, render_template_string

bp = Blueprint('injection', __name__, url_prefix='/sqli')

metadata = {
    'name': 'SQL Injection',
    'difficulty': 'medium',
    'path': '/sqli',
    'description': 'Classic SQL injection using string formatting.'
}


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(':memory:')
        g.db.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)')
        g.db.executemany('INSERT INTO users (name) VALUES (?)', [('Alice',), ('Bob',)])
    return g.db


@bp.route('/')
def index():
    user = request.args.get('id', '1')
    db = get_db()
    query = f"SELECT name FROM users WHERE id = {user}"
    try:
        row = db.execute(query).fetchone()
        name = row[0] if row else 'Not found'
    except sqlite3.Error as exc:
        name = str(exc)
    return render_template_string('<p>User: {{name}}</p>', name=name)
