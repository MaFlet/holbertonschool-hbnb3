from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, send_from_directory,
    flash, current_app, jsonify, session
)
from typing import Union
from werkzeug.wrappers import Response
from sqlalchemy.exc import SQLAlchemyError
from functools import wraps
import secrets
from datetime import datetime
from app import bcrypt
from app.models.user import User
from app.models.place import Place
from app.persistence import db_session
import os

app = Blueprint('app', __name__)


# Serving static login 
def login_required(f):
    """Check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first.', 'error')
            return redirect(url_for('app.login'))
        return f(*args, **kwargs)
    return decorated_function

# def admin_required(f):
#     """Checking is user is admin"""
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not session.get('is_admin', False):
#             flash('Admin access required.', 'error')
#             return redirect(url_for('app.index'))
#         return f(*args, **kwargs)
#     return decorated_function

def serve_static_html(filename):
    """Helper function to serve static HTML files"""
    return send_from_directory(
        os.path.join(current_app.root_path, 'templates'),
        filename
    )

@app.route('/')
def index():
    """Handling index page"""
    return send_from_directory('templates', 'index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login"""
    if request.method == 'GET':
        return send_from_directory('templates', 'login.html')
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            email = data.get('email', '').lower().strip()
            password = data.get('password')

            if not email or not password:
                return jsonify({
                    'message': 'Email and password are required.',
                    'status': 'error'
                }), 400

            user = db_session.query(User).filter(User._email == email).first() # using User's model query

            if user and user.verify_password(password):
                session['user_id'] = user.id
                session['is_admin'] = user.is_admin
                return jsonify({
                    'message': 'Successfully logged in!',
                    'redirect': '/'
                })
            
            return jsonify({
                'message': 'Invalid email or password.',
                'redirect': '/'
            }), 401
        
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error during login: {str(e)}")
            return jsonify({
                'message': 'Database error occurred. Please try again.',
                'status': 'error'
            }), 500

@app.route('/register', methods=['GET'])
def register() -> str:
    """Handling in displaying registration page"""
    if 'user_id' in session:
        return redirect(url_for('app.index'))
    return render_template('register.html')

@app.route('/register-visitor', methods=['POST'])
def register_visitor() -> Response:
    """Handling visitor registration"""
    print("Form data received:", request.form)
    try:
        first_name = request.form.get('firstName', '').strip()
        last_name = request.form.get('lastName', '').strip()
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password')

        if not all([first_name, last_name, email, password]):
            flash('All required fields must be filled.', 'error')
            return redirect(url_for('app.register'))
        
        existing_user = db_session.query(User).filter(User._email == email).first()
        if existing_user:
            flash('Email already registered', 'error')
            return redirect(url_for('app.register'))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
        )
        db_session.add(new_user)
        db_session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('app.login'))
    
    except SQLAlchemyError as e:
        db_session.rollback()
        current_app.logger.error(f"Database error during visitor registration: {str(e)}")
        flash('Database error occurred. Please try again.', 'error')
        return redirect(url_for('app.register'))
    
@app.route('/register-owner', methods=['POST'])
def register_owner() -> Response:
    """Handling owner registration"""
    try:
        first_name = request.form.get('firstName', '').strip()
        last_name = request.form.get('lastName', '').strip()
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password')

        title = request.form.get('placeName', '').strip()
        description = request.form.get('placeType', '').strip()
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        price = request.form.get('price', 0.0)

        if not all([first_name, last_name, email, password, title,
                    description, latitude, longitude, price]):
            flash('All required fields must be filled.', 'error')
            return redirect(url_for('app.register'))
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            price = float(price)
            if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
                flash('Invalid coordinates.', 'error')
                return redirect(url_for('app.register'))
        except ValueError:
            flash('Invalid coordinate format.', 'error')
            return redirect(url_for('app.register'))
        
        existing_user = db_session.query(User).filter(User._email == email).first()
        if existing_user:
            flash('Email already registered.', 'error')
            return redirect(url_for('app.register'))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
        )
        db_session.add(new_user)
        db_session.flush()

        new_place = Place(
            title=title,
            description=description,
            price=price,
            latitude=latitude,
            longitude=longitude,
            owner_id=new_user.id
        )
        db_session.add(new_place)
        db_session.commit()
        flash('Registration successful! Please log in again.', 'success')
        return redirect(url_for('app.login'))
    
    except SQLAlchemyError as e:
        db_session.rollback()
        current_app.logger.error(f"Database error during owner registration: {str(e)}")
        flash('Database error occurred. Please try again.', 'error')
        return redirect(url_for('app.register'))
    

@app.route('/logout')
def logout() -> Response:
    session.clear()
    flash('Successfully logged out!', 'success')
    return redirect(url_for('index'))

# @app.route('/admin')
# @login_required
# @admin_required
# def admin():
#     """Handling admin page"""
#     return render_template('admin.html')

# Explicit route for serving static files (fallback)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('templates', filename)
