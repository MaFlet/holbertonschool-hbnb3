from flask import Flask, Blueprint, render_template, request
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from app.config import config
import os


bcrypt = Bcrypt()


def create_app(config_name='default'):
    """ method used to create an app instance """
    app = Flask(__name__,
                static_url_path='/static', # This makes static files serve from root
                static_folder='static',
                template_folder='templates')
    
    #Upload images configurations
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.config.from_object(config[config_name])
    app.config['DEBUG'] = True

    # Initialize extensions
    CORS(app, supports_credentials=True)
    bcrypt.init_app(app)

    # Initialize database
    from app.persistence import init_db
    init_db()

    # Register web routes blueprint
    from app.routes import app as routes_bp
    app.register_blueprint(routes_bp)

    # Create Blueprint for API
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API Documentation',
        doc='/docs',
    )

    # Import API namespaces
    try:
        # Register API blueprint
        from app.api.v1.users import api as users_ns
        from app.api.v1.amenities import api as amenities_ns
        from app.api.v1.places import api as places_ns
        from app.api.v1.reviews import api as reviews_ns

 
        api.add_namespace(users_ns, path='/users')
        api.add_namespace(amenities_ns, path='/amenities')
        api.add_namespace(places_ns, path='/places')
        api.add_namespace(reviews_ns, path='/reviews')

        app.register_blueprint(api_bp, url_prefix='/api/v1')
    except ImportError as e:
        print(f"Warning: Some API endpoints might not be available: {e}")

    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.error(f'Page not found: {request.url}')
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Server Error: {error}')
        return render_template('errors/500.html'), 500

    return app
