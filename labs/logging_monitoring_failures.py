from flask import Blueprint, request

bp = Blueprint('logging_failures', __name__, url_prefix='/logging')

metadata = {
    'name': 'Security Logging and Monitoring Failures',
    'difficulty': 'easy',
    'path': '/logging',
    'description': 'Login endpoint that ignores and fails to log suspicious activity.'
}

@bp.route('/login', methods=['POST'])
def login():
    # No logging of failed attempts
    username = request.form.get('username')
    password = request.form.get('password')
    return f'Login failed for {username}', 401
