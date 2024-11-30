from flask import (
    render_template, request, redirect,
    url_for, session, send_from_directory,
    Blueprint, flash
)
from typing import Union
from werkzeug.wrappers import Response
from sqlalchemy.exc import SQLAlchemyError
from functools import wraps
from app import bcrypt
from app.models.user import User
from app.persistence import db_session


main = Blueprint('main', __name__)

def login_required(f):
    """Check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first.', 'error')
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/login', methods=['GET', 'POST'])
def login() -> Union[str, Response]:
    """Handles user login"""
    if 'user_id' in session:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            password = request.form.get('password')

            if not email or not password:
                flash('Email and password are required.', 'error')
                return render_template('login.html')

            user = db_session.query(User).filter(User._email == email).first() # using User's model query

            if user and user.verify_password(password):
                session['user_id'] = user.id
                session['is_admin'] = user.is_admin
                flash('Successfully logged in!', 'success')
                return redirect(url_for('main.index'))
            flash('Invalid email or password.', 'error')
            return render_template('login.html')
        except SQLAlchemyError as e:
            flash('Database error occurred. Please try again.', 'error')
            return render_template('login.html')
        
    return render_template('login.html')

@main.route('/logout')
def logout() -> Response:
    session.clear()
    flash('Successfullt logged out!', 'success')
    return redirect(url_for('main.index'))

@main.route('/')
def index() -> str:
    print("flaskindex")
    # is_authenticated = 'user_id' in session
    # if is_authenticated:
    #     user = db_session.query(User).filter(User.id == session['user_id']).first()
    #     return send_from_directory('index.html',
    #                            is_authenticated=is_authenticated,
    #                            user=user)
    return send_from_directory('templates', 'index.html')
