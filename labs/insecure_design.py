from flask import Blueprint, request, redirect

bp = Blueprint('insecure_design', __name__, url_prefix='/redirect')

metadata = {
    'name': 'Insecure Design',
    'difficulty': 'easy',
    'path': '/redirect',
    'description': 'Open redirect allowing arbitrary URL redirection.'
}

@bp.route('/')
def redirector():
    url = request.args.get('url', '/')
    return redirect(url)
