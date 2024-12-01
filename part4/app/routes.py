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
from app.models.place import Place
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

@main.route('/register', methods=['GET'])
def register() -> str:
    """Handling in displaying registration page"""
    if 'user_id' in session:
        return redirect(url_for('main.index'))
    return render_template('register.html')

@main.route('/register-visitor', methods=['POST'])
def register_visitor() -> Response:
    """Handling visitor registration"""
    try:
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')

        if not all([first_name, last_name, email, password]):
            flash('All required fields must be filled.', 'error')
            return redirect(url_for('main.register'))
        existing_user = db_session.query(User).filter(User.email == email).first()
        if existing_user:
            flash('Email already registered', 'error')
            return redirect(url_for('main.register'))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            user_type='visitor'
        )
        db_session.add(new_user)
        db_session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('main.login'))
    
    except SQLAlchemyError as e:
        db_session.rollback()
        flash('Database error occurred. Please try again.', 'error')
        return redirect(url_for('main.register'))
    
@main.route('/register-owner', methods=['POST'])
def register_owner() -> Response:
    """Handling owner registration"""
    try:
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')

        place_name = request.form.get('placeName')
        place_type = request.form.get('placeType')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        if not all([first_name, last_name, email, password, place_name,
                    place_type, latitude, longitude]):
            flash('All required fields must be filled.', 'error')
            return redirect(url_for('main.register'))
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
                flash('Invalid coordinates.', 'error')
                return redirect(url_for('main.register'))
        except ValueError:
            flash('Invalid coordinate format.', 'error')
            return redirect(url_for('main.register'))
        
        existing_user = db_session.query(User).filter(User._email == email).first()
        if existing_user:
            flash('Email already registered.', 'error')
            return redirect(url_for('main.register'))
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            user_type='owner'
        )
        db_session.add(new_user)
        db_session.flush()

        new_place = Place(
            name=place_name,
            type=place_type,
            latitude=latitude,
            longitude=longitude,
            owner_id=new_user.id
        )
        db_session.add(new_place)
        db_session.commit()
        flash('Registration successful! Please log in again.', 'success')
        return redirect(url_for('main.login'))
    
    except SQLAlchemyError as e:
        db_session.rollback()
        flash('Database error occurred. Please try again.', 'error')
        return redirect(url_for('main.register'))
    
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
