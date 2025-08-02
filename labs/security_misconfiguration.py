import os
from flask import Blueprint

bp = Blueprint('security_misconfiguration', __name__, url_prefix='/config')

metadata = {
    'name': 'Security Misconfiguration',
    'difficulty': 'easy',
    'path': '/config',
    'description': 'Exposes environment variables to the user.'
}

@bp.route('/env')
def show_env():
    items = '<br>'.join(f'{k}={v}' for k, v in os.environ.items())
    return items
