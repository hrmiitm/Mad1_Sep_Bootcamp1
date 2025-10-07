from flask import Flask, render_template, request, url_for, redirect, session, flash
from models import db, User


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

def get_curr_user() -> User | None:
    user_id = session.get('id')
    user = User.query.filter_by(id = user_id).first()
    return user


@app.route('/')
def home():
    user = get_curr_user()
    return render_template('home.html', user=user)

# render the view
@app.route('/access')
def access():
    user = get_curr_user()
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)