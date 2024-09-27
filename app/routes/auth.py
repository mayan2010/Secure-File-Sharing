from flask import Blueprint, request, jsonify
from app.services.auth import signup_user, verify_email, login_user

bp = Blueprint('auth', __name__)


@bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    result = signup_user(data['email'], data['password'])
    return jsonify(result), result['status_code']


@bp.route('/verify-email/<token>', methods=['GET'])
def verify(token):
    result = verify_email(token)
    return jsonify(result), result['status_code']


@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    result = login_user(data['email'], data['password'])
    return jsonify(result), result['status_code']
