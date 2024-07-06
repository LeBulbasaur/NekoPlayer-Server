import os
import json
from flask import Blueprint, request, jsonify, send_from_directory
from database import db
from models import Song
from werkzeug.utils import secure_filename
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

handle_songs = Blueprint('handle_songs', __name__)

@handle_songs.route('/songs', methods=['GET'])
def get_songs():
    songs = Song.query.all()
    songs = [{
        'id': song.id,
        'title': song.title, 
        'artist': song.artist, 
        'release_date': song.release_date,
        'user_id': song.user_id,
        'cover_path': song.cover_path, 
        'song_path': song.song_path} for song in songs]
    return jsonify({'songs': songs})

@handle_songs.route('/songs', methods=['POST'])
@jwt_required()
def create_song():
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({'error': 'Unauthorized'}), 401
    
    song_data = request.form['song_data']
    song_data = json.loads(song_data)

    songs = Song.query.all()

    song_file = request.files['song_file']
    song_file_name = str(len(songs) + 1) + '_' + secure_filename(song_file.filename)
    song_file.save(os.path.join(os.getcwd(), 'static', 'songs', song_file_name))

    cover_image = request.files['cover_image']
    cover_image_name = str(len(songs) + 1) + '_' + secure_filename(cover_image.filename)
    cover_image.save(os.path.join(os.getcwd(), 'static', 'covers', cover_image_name))
    

    song = Song(
        title=song_data['title'], 
        artist=song_data['artist'], 
        release_date=song_data['release_date'],
        user_id=current_user, 
        cover_path=cover_image_name, 
        song_path=song_file_name)
    db.session.add(song)
    db.session.commit()
    return jsonify({'message': 'Song created!'})

@handle_songs.route('/songs/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_song(id):
    song = Song.query.get(id)
    if not song:
        return jsonify({'error': 'Song not found'}), 404
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({'error': 'Unauthorized'}), 401
    if song.user_id != current_user and current_user != 1:
        return jsonify({'error': 'Unauthorized'}), 401
    for playlist in song.playlists:
        playlist.songs.remove(song)
        print(playlist)
    os.remove(os.path.join(os.getcwd(), 'static', 'songs', song.song_path))
    os.remove(os.path.join(os.getcwd(), 'static', 'covers', song.cover_path))
    db.session.delete(song)
    db.session.commit()
    return jsonify({'message': 'Song deleted!'})


@handle_songs.route('/songs/cover/<string:cover_path>', methods=['GET'])
def get_cover(cover_path):
    return send_from_directory(os.path.join(os.getcwd(), 'static', 'covers'), cover_path)

@handle_songs.route('/songs/file/<string:song_path>', methods=['GET'])
def get_song(song_path):
    return send_from_directory(os.path.join(os.getcwd(), 'static', 'songs'), song_path)