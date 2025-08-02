from flask import Blueprint, request, render_template_string, session

bp = Blueprint('auth_failures', __name__, url_prefix='/auth')

metadata = {
    'name': 'Identification and Authentication Failures',
    'difficulty': 'easy',
    'path': '/auth',
    'description': 'Hardcoded credentials with no protections.'
}

@bp.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        if request.form.get('username') == 'admin' and request.form.get('password') == 'password':
            session['user'] = 'admin'
            return 'Logged in as admin'
        error = 'Invalid credentials'
    return render_template_string(
        '<form method="post"><input name="username"><input name="password" type="password"><input type="submit"></form>'
        '<p>{{error}}</p>', error=error
    )
