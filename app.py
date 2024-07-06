from flask import Flask 
from flask_cors import CORS
from database import db
from config import Config
from flask_jwt_extended import JWTManager
from models import User, Playlist
from werkzeug.security import generate_password_hash
from blueprints.handle_songs import handle_songs
from blueprints.handle_auth import handle_auth
from blueprints.handle_users import handle_users
from blueprints.handle_playlists import handle_playlists

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(handle_songs)
app.register_blueprint(handle_auth)
app.register_blueprint(handle_users)
app.register_blueprint(handle_playlists)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            hashed_password = generate_password_hash('admin', method='pbkdf2')
            admin = User(username='admin', password=hashed_password, role='admin', picture_path='default.jpg')
            db.session.add(admin)
            db.session.commit() 
            playlist = Playlist(default_playlist=True,name='admin', user_id=admin.id, songs=[], cover_path='default.png')
            db.session.add(playlist)
            db.session.commit() 
    app.run()