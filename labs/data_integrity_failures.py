import pickle
from flask import Blueprint, request

bp = Blueprint('data_integrity_failures', __name__, url_prefix='/pickle')

metadata = {
    'name': 'Software and Data Integrity Failures',
    'difficulty': 'medium',
    'path': '/pickle',
    'description': 'Deserializes user input using pickle without validation.'
}

@bp.route('/load', methods=['POST'])
def load():
    data = request.data
    obj = pickle.loads(data)  # Insecure
    return str(obj)
