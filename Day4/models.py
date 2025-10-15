from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Secondary Table For Many To Many Relationship
SongInPlaylist = db.Table(
    'song_in_playlist',
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key=True),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key=True)
)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    isBlacklisted = db.Column(db.Boolean, default=False)

    # RBAC
    isUser = db.Column(db.Boolean, default=True)
    isCreator = db.Column(db.Boolean, default=False)
    isAdmin = db.Column(db.Boolean, default=False)

    # One To Many Relationship
    songs = db.relationship('Song', backref='user', lazy=True)
    playlist = db.relationship('Playlist', backref='user', lazy=True)

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # One To May Realtionship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    lyrics = db.Column(db.String, default='')
    duration = db.Column(db.String, default='')
    date = db.Column(db.String, default='')
    rating = db.Column(db.String, default='')

    isBlacklisted = db.Column(db.Boolean, default=False)

    # One To Many Relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Many To Many Relationship
    playlists = db.relationship('Playlist', secondary=SongInPlaylist, backref=db.backref('songs', lazy=True))

