import requests
from flask import Blueprint, request

bp = Blueprint('ssrf', __name__, url_prefix='/ssrf')

metadata = {
    'name': 'Server-Side Request Forgery',
    'difficulty': 'hard',
    'path': '/ssrf',
    'description': 'Fetches URLs provided by the user without validation.'
}

@bp.route('/')
def fetch():
    url = request.args.get('url', 'http://localhost')
    resp = requests.get(url)
    return resp.text[:200]
