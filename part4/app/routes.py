from flask import render_template, request, redirect, url_for, session
from app import app, bcrypt
from app.models.user import User
# from app.persistence import db_session


bcrypt = Bcrypt()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = db_session.query(User).filter(User._email == email).first() # using User's model query

        if user and user.verify_password(password):
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid email or password')
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/')
def index():
    is_authenticated = 'user_id' in session
    if is_authenticated:
        user = db_session.query(User).filter(User.id == session['user_id']).first()
        return render_template('index.html',
                               is_authenticated=is_authenticated,
                               user=user)
    return render_template('index.html', is_authenticated=False)
