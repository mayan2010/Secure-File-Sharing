from flask import current_app
from app import mongo
from app.models import User
import jwt
import datetime
from bson.objectid import ObjectId


def signup_user(email, password):
    existing_user = mongo.db.users.find_one({'email': email})
    if existing_user:
        return {'message': 'User already exists!'}, 400

    new_user = User(email, password)
    result = new_user.save()

    verification_token = jwt.encode({
        'user_id': str(result.inserted_id),
        'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=24)
    }, current_app.config['SECRET_KEY'])

    # TODO: Send verification email with the token
    verification_url = f"http://127.0.0.1:5000/verify-email/{verification_token}"

    return {'message': 'User created successfully. '
                       'Check your email for verification link. '
                       'It will expire in 24 hours.',
            'verification_url': verification_url}, 201


def verify_email(token):
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        user = mongo.db.users.find_one({'_id': ObjectId(data['user_id'])})
        if user:
            mongo.db.users.update_one({'_id': ObjectId(data['user_id'])}, {'$set': {'verified': True}})
            return {'message': 'Email verified successfully'}, 200
        else:
            return {'message': 'User not found'}, 404
    except jwt.ExpiredSignatureError:
        return {'message': 'Verification link has expired'}, 400
    except jwt.InvalidTokenError:
        return {'message': 'Invalid verification link'}, 400


def login_user(email, password):
    user = mongo.db.users.find_one({'email': email})
    if user and User.check_password(user['password'], password):
        if user['role'] == 'client' and not user['verified']:
            return {'message': 'Please verify your email first'}, 401
        token = jwt.encode({
            'user_id': str(user['_id']),
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'])
        return {'token': token}, 200
    return {'message': 'Invalid credentials'}, 401
