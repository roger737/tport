from flask import Blueprint, request, session, redirect

bp = Blueprint('broken_access_control', __name__, url_prefix='/broken_access')

metadata = {
    'name': 'Broken Access Control',
    'difficulty': 'easy',
    'path': '/broken_access',
    'description': 'Role can be set via query parameter allowing admin access.'
}

@bp.route('/login')
def login():
    role = request.args.get('role', 'user')
    session['role'] = role
    return redirect('/broken_access/admin')

@bp.route('/admin')
def admin():
    if session.get('role') != 'admin':
        return 'Forbidden', 403
    return 'Welcome, admin!'
