from flask import render_template, request, redirect, url_for, session
from app import app
from app.models import User
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
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
    return render_template('index.html', is_authenticated=is_authenticated)
