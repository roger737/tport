import flask
from flask import Blueprint, render_template_string

bp = Blueprint('vulnerable_components', __name__, url_prefix='/components')

metadata = {
    'name': 'Vulnerable and Outdated Components',
    'difficulty': 'easy',
    'path': '/components',
    'description': 'Displays the version of Flask which may be outdated.'
}

@bp.route('/')
def index():
    return render_template_string('<p>Flask version: {{v}}</p>', v=flask.__version__)
