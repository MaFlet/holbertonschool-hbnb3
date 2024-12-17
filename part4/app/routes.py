import uuid
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, send_from_directory,
    flash, current_app, jsonify, session
)
from typing import Union
from werkzeug.wrappers import Response
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError
from functools import wraps
import secrets
from datetime import datetime
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.persistence import db_session
import os

app = Blueprint('app', __name__)

UPLOAD_FOLDER = 'app/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

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

def allowed_file(filename):
    """Check if the file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Handling index page"""
    return render_template('index.html')
    # except Exception as e:
    #     current_app.logger.error(f"Error serving index page: {str(e)}")
    #     return "Error loading page", 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login"""
    if request.method == 'GET':
        return render_template('login.html')
        # except Exception as e:
        #     current_app.logger.error(f"Error serving login page: {str(e)}")
        #     return "Error loading login page", 500
    
    if request.method == 'POST':
        try:
            # Handle both JSON and form data
            if request.is_json:
                data = request.get_json()
                email = data.get('email', '').lower().strip()
                password = data.get('password')
            else:
                email = request.form.get('email', '').lower().strip()
                password = request.form.get('password')

            if not email or not password:
                message = 'Email and password are required.'
                return (jsonify({'message': message, 'status': 'error'}), 400) if request.is_json else (
                    render_template('login.html', error=message))

            user = db_session.query(User).filter(User._email == email).first() # using User's model query

            if user and user.verify_password(password):
                session['user_id'] = user.id
                session['is_admin'] = user.is_admin
                session['login_time'] = datetime.now().isoformat()

                if request.is_json:
                    return jsonify({
                    'message': 'Successfully logged in!',
                    'redirect': '/'
                })
                flash('Successfully logged in!', 'success')
                return redirect(url_for('app.index'))
            
            message = 'Invalid email or password.'
            return (jsonify({'message': message, 'status': 'error'}), 500) if request.is_json else (
                render_template('login.html', error=message))
        
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error during login: {str(e)}")
            message = 'Database error occurred. Please try again.'
            return (jsonify({'message': message, 'status': 'error'}), 500) if request.is_json else (
                render_template('login.html', error=message))
        
@app.route('/register', methods=['GET'])
def register() -> str:
    """Handling in displaying registration page"""
    if 'user_id' in session:
        return redirect(url_for('app.index'))
    return render_template('register.html')

@app.route('/owner-register', methods=['GET'])
def owner_register() -> str:
    """Handle displaying owner registration page"""
    if 'user_id' in session:
        return redirect(url_for('app.index'))
    return render_template('owner-register.html')

@app.route('/register-visitor', methods=['POST'])
def register_visitor() -> Response:
    """Handling visitor registration"""
    try:
        first_name = request.form.get('firstName', '').strip()
        last_name = request.form.get('lastName', '').strip()
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password')

        if not all([first_name, last_name, email, password]):
            flash('All required fields must be filled.', 'error')
            return redirect(url_for('app.register'))
        
        try:
            # Create new user - the model will handle validation
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                is_admin=False
            )
            # Add to database
            db_session.add(new_user)
            db_session.commit()

            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('app.login'))
        
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('app.register'))
    
    except SQLAlchemyError as e:
        db_session.rollback()
        current_app.logger.error(f"Database error during visitor registration: {str(e)}")
        flash('Database error occurred. Please try again.', 'error')
        return redirect(url_for('app.register'))
    
@app.route('/register-owner', methods=['POST'])
def register_owner() -> Response:
    """Handling owner registration"""
    try:
        # Getting form data
        data = request.form
        files = request.files.getlist('photos')

        # Validate file uploads
        if not files or files[0].filename == '':
            flash('At least one image is required', 'error')
            return redirect(url_for('app.register'))

        # Process and save images
        image_paths = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Create a unique filename to avoid conflicts
                unique_filename = f"{uuid.uuid4()}_{filename}"
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                # Store the path relative to static folder
                relative_path = f"/static/images/{unique_filename}"
                image_paths.append(relative_path)
            else:
                flash('Invalid file type. Allowed types are: pnj, jpg, jpeg, gif', 'error')
                return redirect(url_for('app.register'))
                
        # Get user data
        first_name = request.form.get('firstName', '').strip()
        last_name = request.form.get('lastName', '').strip()
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password')

        # Get place data
        title = request.form.get('placeName', '').strip()
        description = request.form.get('placeType', '').strip()
        price = request.form.get('price', type=float)
        latitude = request.form.get('latitude', type=float)
        longitude = request.form.get('longitude', type=float)

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
        
        try:
            # Create new user - the model will handle validation and password hashing
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                is_admin=False
            )

            db_session.add(new_user)
            db_session.flush() # Get the user ID without committing

            # Create new place with images
            new_place = Place(
                title=title,
                description=description,
                price=price,
                latitude=latitude,
                longitude=longitude,
                owner_id=new_user.id
            )
            new_place.set_image_paths(image_paths)

            new_user.add_place(new_place)
            db_session.add(new_place)
            db_session.commit()

            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('app.login'))
        
        except ValueError as e:
            db_session.rollback()
            flash(str(e), 'error')
            return redirect(url_for('app.register'))
    
    except SQLAlchemyError as e:
        db_session.rollback()
        current_app.logger.error(f"Database error during owner registration: {str(e)}")
        flash('Database error occurred. Please try again.', 'error')
        return redirect(url_for('app.register'))
    
@app.route('/place')
def place():
    """Handle displaying place details page"""
    try:
        return send_from_directory('templates', 'place.html')
    except Exception as e:
        current_app.logger.error(f"Error serving place page: {str(e)}")
        return "Error loading page", 500
    
# @app.route('/place/<place_id>')
# def place_details(place_id):
#     """Handle displaying place details page"""
#     try:
#         # Get place details from database
#         place = db_session.query(Place).get(place_id)
#         if not place:
#             flash('Place not found', 'error')
#             return redirect(url_for('app.index'))
#          # Get reviews for this place
#         reviews = db_session.query(Review).filter_by(place_id=place_id).all()
#          # Pass both place and reviews to the template
#         return render_template('place.html', place=place, reviews=reviews)
#     except SQLAlchemyError as e:
#         current_app.logger.error(f"Database error: {str(e)}")
#         flash('Error loading place details', 'error')
#         return redirect(url_for('app.index'))

@app.route('/place/<place_id>')
def place_details(place_id):
    """Handle displaying place details page"""
    try:
        # Get place details from database
        place = db_session.query(Place).get(place_id)
        if not place:
            flash('Place not found', 'error')
            return redirect(url_for('app.index'))
        
        # Get reviews for this place
        reviews = db_session.query(Review).filter_by(place_id=place_id).all()
        
        # Pass both place and reviews to the template
        return render_template('place.html', place=place, reviews=reviews)
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error: {str(e)}")
        flash('Error loading place details', 'error')
        return redirect(url_for('app.index'))
    
@app.route('/api/v1/places/')
def get_places():
    try:
        places = db_session.query(Place).all()
        return jsonify([{
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'image_paths': place.get_image_paths(),
            'owner_id': place.owner_id
        } for place in places])
    except Exception as e:
        current_app.logger.error(f"Error fetching places: {str(e)}")
        return jsonify({'error': 'Error fetching places'}), 500

@app.route('/logout')
def logout() -> Response:
    session.clear()
    flash('Successfully logged out!', 'success')
    return redirect(url_for('index'))

@app.route('/add-review/<string:place_id>')
@login_required  # Make sure user is logged in
def add_review_page(place_id):
    place = db_session.query(Place).get(place_id)
    if not place:
        flash('Place not found', 'error')
        return redirect(url_for('index'))
    return render_template('add_review.html', place=place)

@app.route('/api/v1/places/<string:place_id>/reviews', methods=['GET', 'POST'])
@login_required
def place_reviews(place_id):
    if request.method == 'GET':
        reviews = db_session.query(Review).filter_by(place_id=place_id).all()
        # return jsonify([{
        #     'id': review.id,
        #     'text': review.text,
        #     'rating': review.rating,
        #     'user': {
        #         'first_name': review.user.first_name,
        #         'last_name': review.user.last_name
        #     }
        # } for review in reviews])
        return jsonify(reviews=reviews)
    elif request.method == 'POST':
        data = request.get_json()
        new_review = Review(
            text=data['text'],
            rating=data['rating'],
            place_id=place_id,
            user_id=session['user_id']
        )
        db_session.add(new_review)
        db_session.commit()
        return jsonify({'message': 'Review added successfully'})

def add_review(place_id):
    try:
        data = request.get_json()
        new_review = Review(
            text=data['text'],
            rating=data['rating'],
            place_id=place_id,
            user_id=session['user_id']
        )
        db_session.add(new_review)
        db_session.commit()
        return jsonify({'message': 'Review added successfully'}), 200
    except Exception as e:
        db_session.rollback()
        return jsonify({'error': str(e)}), 500

# @app.route('/admin')
# @login_required
# @admin_required
# def admin():
#     """Handling admin page"""
#     return render_template('admin.html')

# Explicit route for serving static files (fallback)
@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    try:
        return send_from_directory('static', filename)
    except Exception as e:
        current_app.logger.error(f"Error serving static file {filename}: {str(e)}")
        return "File not found", 404
