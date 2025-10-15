from flask import Flask, render_template, request, url_for, redirect, session, flash
from models import db, User, Song
import os

app = Flask(__name__)


# Database
# 1) Config
# 2) Models

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = '123'

# To Connect with db
db.init_app(app)
app.app_context().push() # allow database operation
db.create_all() # Create/update schema

def get_current_user() -> User | None:
    user_id = session.get('id')
    user = User.query.filter_by(id = user_id).first()
    return user


@app.route('/')
def home():
    user = get_current_user()
    return render_template('home.html', user=user)


# ======================Login/Logout/Register============================
# render the view
@app.route('/access')
def access():
    user = get_current_user()
    return render_template('access.html', user=user)

# operation done on view
# <form action="/login" method="POST">
@app.route("/login", methods=["POST"])
def login():
    # Get data
    email = request.form.get('email')
    password = request.form.get('password')\
    
    # Validate Data
    user = User.query.filter_by(email = email) # rows = [<u1>, <u2>, ...]
    user = User.query.filter_by(email = email).first() # row = <u1>

    if user and user.password == password:
        session['id'] = user.id
        flash("Login Successful", "success")
        return redirect(url_for('home'))
    else:
        flash("Either email or password incorrect", "danger")
        return redirect(url_for('access'))
    
# <form action="/register" method="POST">
@app.route("/register", methods=["POST"])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2') # 'sadfa', '', None
    
    user = User.query.filter_by(email = email).first() # row = <u1>

    if not user and password1 == password2 and password1 != None and password1 != '':
        u = User(name=name, email=email, password=password1)
        db.session.add(u)
        db.session.commit()
        flash('New user created, Now please Login', 'success')
    else:
        flash('User already exists or some field not provided', 'danger')

    return redirect(url_for('access'))

@app.route('/logout')
def logout():
    session.pop('id', None)
    flash('Logout Successful', 'success')
    return redirect(url_for('access'))
# =======================================================================
# =========================SongCrudByCreator=============================
# /songs
# /songs?song_id=3
@app.route('/songs')
def songs(): # this will return HTML
    user = get_current_user() # <user>/None
    songs = user.songs
    albums = []

    song_id = request.args.get('songs_id', None)
    song = None
    if song_id:
        song = Song.query.filter_by(id=song_id).first()

    return render_template('songs.html', user=user, songs=songs, song=song, albums=albums)

# Below route will -> do operation --> redirect songs
@app.route('/upload_song', methods=['POST'])
def upload_song():
    user = get_current_user()
    data = request.form
   

    name = data.get('name')
    lyrics = data.get('lyrics')
    duration = data.get('duration')
    date = data.get('date')

    file = request.files.get('file')

    # Validation
    # Save the Info 
    # 1) database
    # 2) Direcetory
    song_obj = Song(name=name, lyrics=lyrics, duration=duration, date=date, user_id=user.id)
    db.session.add(song_obj)
    db.session.commit()

    filename=f'{song_obj.id}.mp3' # 1.mp3
    file.save(os.path.join('./static/songs/', filename))
    flash('Song Created Successfully', 'success')


    return redirect(url_for('songs'))

@app.route('/update_song', methods=['POST'])
def update_song():
    data = request.form
    print(data)
    return redirect(url_for('songs'))

@app.route('/delete_song') # /delete_song?song_id=4
def delete_song():
    song_id = request.args.get('song_id')
    user = get_current_user()

    # Validation & Deletion
    song_obj = Song.query.filter_by(id=song_id).first()
    if song_obj:
        if song_obj.user.id == user.id:
            
            db.session.delete(song_obj)
            db.session.commit()

            os.remove(os.path.join('./static/songs/', f'{song_id}.mp3'))

            flash('Song Deleted', 'success')
        else:
            flash('You are not creator of this song. So Access Denied', 'danger')
    else:
        flash('Song Not Found', 'danger')

    return redirect(url_for('songs'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)