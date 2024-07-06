import os
from database import db
from flask import Blueprint, request, jsonify, send_from_directory
from models import Playlist, Song
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

handle_playlists = Blueprint('handle_playlists', __name__)

def serialize(playlist):
    return {
        'id': playlist.id,
        'default_playlist': playlist.default_playlist,
        'name': playlist.name,
        'user_id': playlist.user_id,
        'cover_path': playlist.cover_path,
        'songs': [serialize_song(song) for song in playlist.songs]
    }

def serialize_song(song):
    return {
        'id': song.id,
        'title': song.title, 
        'artist': song.artist, 
        'release_date': song.release_date,
        'user_id': song.user_id,
        'cover_path': song.cover_path, 
        'song_path': song.song_path
    }

@handle_playlists.route('/playlist', methods=['GET'])
def get_playlists():
    playlists = Playlist.query.all()
    return jsonify([serialize(playlist) for playlist in playlists]), 200

@handle_playlists.route('/playlist/<int:id>', methods=['GET'])
def get_playlist(id):
    playlist = Playlist.query.get(id)
    if not playlist:
        return jsonify({'error': 'Playlist not found'}), 404
    return jsonify(serialize(playlist)), 200

@handle_playlists.route('/playlist/cover/<string:cover_path>', methods=['GET'])
def get_cover(cover_path):
    return send_from_directory(os.path.join(os.getcwd(), 'static', 'playlists'), cover_path)

@handle_playlists.route('/playlist', methods=['POST'])
@jwt_required()
def create_playlist():
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({'error': 'Unauthorized'}), 401
    
    name = request.form['name']

    playlists = Playlist.query.all()

    for playlist in playlists:
        if playlist.name == name:
            return jsonify({'error': 'Playlist name already taken'}), 400

    cover_image = request.files['cover_image']
    cover_image_name = str(len(playlists) + 1) + '_' + secure_filename(cover_image.filename)
    cover_image.save(os.path.join(os.getcwd(), 'static', 'playlists', cover_image_name))

    current_user = get_jwt_identity()
    playlist = Playlist(
        name=name,
        user_id=current_user,
        songs=[],
        cover_path=cover_image_name)
    db.session.add(playlist)
    
    try:
        db.session.commit()
    except IntegrityError:
        return jsonify({'error': 'Playlist name already taken'}), 400
    return jsonify(serialize(playlist)), 201

@handle_playlists.route('/playlist/song/<int:id>', methods=['POST'])
@jwt_required()
def create_playlist_with_song(id):
    name = request.form['name']

    playlists = Playlist.query.all()

    cover_image = request.files['cover_image']
    cover_image_name = str(len(playlists) + 1) + '_' + secure_filename(cover_image.filename)
    cover_image.save(os.path.join(os.getcwd(), 'static', 'playlists', cover_image_name))

    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({'error': 'Unauthorized'}), 401
    playlist = Playlist(
        name=name,
        user_id=current_user,
        songs=[Song.query.get(id)],
        cover_path=cover_image_name)
    db.session.add(playlist)

    try:
        db.session.commit()
    except IntegrityError:
        return jsonify({'error': 'Playlist name already taken'}), 400
    return jsonify({'message': 'Playlist created'}), 201

@handle_playlists.route('/playlist/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_playlist(id):
    playlist = Playlist.query.get(id)
    if not playlist:
        return jsonify({'error': 'Playlist not found'}), 404
    if playlist.user_id != get_jwt_identity() and get_jwt_identity() != 1:
        return jsonify({'error': 'Unauthorized'}), 401
    if playlist.cover_path != 'default.png':
        os.remove(os.path.join(os.getcwd(), 'static', 'playlists', playlist.cover_path))
    db.session.delete(playlist)
    db.session.commit()
    return jsonify({'message': 'Playlist deleted'}), 200

@handle_playlists.route('/playlist/<int:id>/song/<int:song_id>', methods=['PUT'])
@jwt_required()
def add_song_to_playlist(id, song_id):
    playlist = Playlist.query.get(id)
    if not playlist:
        return jsonify({'error': 'Playlist not found'}), 404
    if playlist.user_id != get_jwt_identity() and get_jwt_identity() != 1:
        return jsonify({'error': 'Unauthorized'}), 401
    song = Song.query.get(song_id)
    if not song:
        return jsonify({'error': 'Song not found'}), 404
    if song in playlist.songs:
        return jsonify({'error': 'Song already in playlist'}), 400
    playlist.songs.append(song)
    db.session.commit()
    return jsonify({'message': 'Song added to playlist'}), 201

@handle_playlists.route('/playlist/<int:id>/song/<int:song_id>', methods=['DELETE'])
@jwt_required()
def remove_song_from_playlist(id, song_id):
    playlist = Playlist.query.get(id)
    if not playlist:
        return jsonify({'error': 'Playlist not found'}), 404
    if playlist.user_id != get_jwt_identity() and get_jwt_identity() != 1:
        return jsonify({'error': 'Unauthorized'}), 401
    song = Song.query.get(song_id)
    if not song:
        return jsonify({'error': 'Song not found'}), 404
    if song not in playlist.songs:
        return jsonify({'error': 'Song not in playlist'}), 400
    playlist.songs.remove(song)
    db.session.commit()
    return jsonify(serialize(playlist)), 200

