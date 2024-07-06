from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_extended import create_access_token

from database import db
from models import User, Playlist

handle_auth = Blueprint('handle_auth', __name__)

@handle_auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already taken'}), 400
    user = User(username=username, password=generate_password_hash(password), picture_path='default.jpg')
    db.session.add(user)
    db.session.commit()
    playlist = Playlist(default_playlist=True,name=username, user_id=user.id, songs=[], cover_path='default.png')
    db.session.add(playlist)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201

@handle_auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid username or password'}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200