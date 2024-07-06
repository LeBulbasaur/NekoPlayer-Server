from database import db, playlist_song

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.Integer, nullable=False)
    cover_path = db.Column(db.String(100), nullable=False)
    song_path = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Nowa relacja
    def __repr__(self):
        return f'<Song {self.title}>'
    
class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    default_playlist = db.Column(db.Boolean, nullable=False, default=False)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Nowa relacja
    songs = db.relationship('Song', secondary=playlist_song, lazy='subquery',
        backref=db.backref('playlists', lazy=True))
    cover_path = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'<Playlist {self.name}>'
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False, default='user')
    songs = db.relationship('Song', backref='user', lazy=True)  # Nowa relacja
    playlists = db.relationship('Playlist', backref='user', lazy=True)  # Nowa relacja
    picture_path = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'<User {self.username}>'