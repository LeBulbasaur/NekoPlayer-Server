from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

playlist_song = db.Table('playlist_song',
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key=True),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key=True)
)