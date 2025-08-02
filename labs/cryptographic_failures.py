import hashlib
from flask import Blueprint, request, render_template_string

bp = Blueprint('cryptographic_failures', __name__, url_prefix='/crypto')

metadata = {
    'name': 'Cryptographic Failures',
    'difficulty': 'easy',
    'path': '/crypto',
    'description': 'Uses weak MD5 hashing for password verification.'
}

# Insecurely stored password hash for user 'admin'
PASSWORD_HASH = hashlib.md5(b'secret').hexdigest()

@bp.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        password = request.form.get('password', '')
        hashed = hashlib.md5(password.encode()).hexdigest()
        if hashed == PASSWORD_HASH:
            return 'Logged in as admin'
        error = 'Incorrect password'
    return render_template_string(
        '<form method="post"><input type="password" name="password"><input type="submit"></form>'
        '<p>{{error}}</p>', error=error
    )
