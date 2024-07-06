import os
from flask import Blueprint, request, jsonify, send_from_directory
from database import db
from models import User
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash

handle_users = Blueprint('handle_users', __name__)

def serialize(user):
    return {
        'id': user.id,
        'username': user.username,
        'picture_path': user.picture_path,
        'role': user.role
    }

@handle_users.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([serialize(user) for user in users]), 200

@handle_users.route('/user/id', methods=['GET'])
@jwt_required()
def get_user_id():
    return jsonify({'id': get_jwt_identity()}), 200

@handle_users.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(serialize(user)), 200

@handle_users.route('/user/<int:id>/photo', methods=['GET'])
def get_user_photo(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return send_from_directory(os.path.join(os.getcwd(), 'static', 'profiles'), user.picture_path)

@handle_users.route('/user/<int:id>/photo', methods=['PUT'])
@jwt_required()
def update_user_photo(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if get_jwt_identity() != id and get_jwt_identity() != 1:
        return jsonify({'error': 'Unauthorized'}), 401
    photo = request.files['photo']
    photo_name = str(id) + '_' + photo.filename
    files = os.listdir(os.path.join(os.getcwd(), 'static', 'profiles'))
    for file in files:
        if file.startswith(str(id)):
            os.remove(os.path.join(os.getcwd(), 'static', 'profiles', file))
    photo.save(os.path.join(os.getcwd(), 'static', 'profiles', photo_name))
    user.picture_path = photo_name
    db.session.commit()
    return jsonify({'message': 'Photo updated'}), 200

@handle_users.route('/user/<int:id>/username', methods=['PUT'])
@jwt_required()
def update_user_username(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if get_jwt_identity() != id and get_jwt_identity() != 1:
        return jsonify({'error': 'Unauthorized'}), 401
    user.username = request.json['username']
    db.session.commit()
    user.playlists[0].name = user.username
    db.session.commit()
    for song in user.songs:
        song.artist = user.username
        db.session.commit()
    return jsonify({'message': 'Username updated'}), 200

@handle_users.route('/user/<int:id>/password', methods=['PUT'])
@jwt_required()
def update_user_password(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if get_jwt_identity() != id and get_jwt_identity() != 1:
        return jsonify({'error': 'Unauthorized'}), 401
    new_password = request.json['new_password']
    user.password = generate_password_hash(new_password)
    db.session.commit()
    return jsonify({'message': 'Password updated'}), 200

@handle_users.route('/user/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if get_jwt_identity() != id and get_jwt_identity() != 1:
        return jsonify({'error': 'Unauthorized'}), 401

    if user.picture_path != 'default.jpg':
        os.remove(os.path.join(os.getcwd(), 'static', 'profiles', user.picture_path))
    for playlist in user.playlists:
        db.session.delete(playlist)
        if playlist.cover_path != 'default.png':
            os.remove(os.path.join(os.getcwd(), 'static', 'playlists', playlist.cover_path))
    for song in user.songs:
        db.session.delete(song)
        os.remove(os.path.join(os.getcwd(), 'static', 'songs', song.song_path))
        os.remove(os.path.join(os.getcwd(), 'static', 'covers', song.cover_path))
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200