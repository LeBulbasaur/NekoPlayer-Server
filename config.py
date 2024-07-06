from datetime import timedelta

class Config(object):
    SECRET_KEY = 'sperek_2024'
    JWT_SECRET_KEY = 'sperek_2024'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///music_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False